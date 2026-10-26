"""Sources and method. Owner: Yajat. Reads everything from data/data_dictionary.yml."""

from datetime import date

import streamlit as st

from utils import data

REPO = "https://github.com/Yajat47/dvn-at3-ai-energy-water/blob/main/"

st.title("Sources and method")
st.markdown(
    f"Every number in this app can be traced to a file in the repository. Data last refreshed: "
    f"**{data.last_refresh()}**. Data moves one way:\n\n"
    "1. **`data/samples/`** holds the source samples: downloads exactly as published, plus "
    "`data/samples/manual/` for numbers copied from report text with the original sentence beside each one.\n"
    "2. **`scripts/build_*.py`** turn samples into processed files. Every step is in code.\n"
    "3. **`data/processed/`** is what the pages read.\n"
    "4. Each chart has a **Where does this number come from?** box listing its sources, files and steps.\n\n"
    f"The full [data dictionary]({REPO}data/DATA_DICTIONARY.md) gives every column, unit, primary key, time "
    "coverage and transform."
)


def table(header: list[str], rows: list[list[str]]) -> None:
    """Markdown table: long cells wrap, so the page never scrolls sideways at 1366x768."""
    def cell(value) -> str:
        return str(value).replace("|", "\\|").replace("\n", " ")

    lines = ["| " + " | ".join(header) + " |", "|" + "---|" * len(header)]
    lines += ["| " + " | ".join(cell(v) for v in row) + " |" for row in rows]
    st.markdown("\n".join(lines))


def made_by(transform) -> str:
    """Link to the build script; a transform written as plain text is shown as it is."""
    if isinstance(transform, dict) and "script" in transform:
        return f"[{transform['script'].removeprefix('scripts/')}]({REPO}{transform['script']})"
    return str(transform)


d = data.dictionary()

st.markdown("### Sources")
table(
    ["Source (ID)", "Publisher", "Licence", "Retrieved"],
    [[f"[{s['title']}]({s['url']}) `{s['id']}`", s["publisher"], s["licence"],
      f"{date.fromisoformat(str(s['retrieved'])):%d %b %Y}".replace(" ", "\u00a0")]
     for s in d["sources"]],
)

st.markdown("### Datasets")
st.markdown("**Source samples** in `data/samples/`, stored as published:")
table(
    ["File", "Primary key", "Time coverage", "Latest"],
    [[f"[{x['path'].removeprefix('data/samples/')}]({REPO}{x['path']})", ", ".join(x["primary_key"]),
      x["time_coverage"], x["latest_observation"]]
     for x in d["datasets"] if x["role"] == "sample"],
)
st.markdown("**Processed files** in `data/processed/`, the files the pages read:")
table(
    ["File", "Made by", "Primary key", "Time coverage", "Latest"],
    [[f"[{x['path'].removeprefix('data/processed/')}]({REPO}{x['path']})",
      made_by(x["transform"]),
      ", ".join(x["primary_key"]), x["time_coverage"], x["latest_observation"]]
     for x in d["datasets"] if x["role"] == "processed"],
)

st.markdown("### Download the processed files")
for f in sorted(data.PROCESSED.glob("*.csv")):
    c1, c2 = st.columns([4, 1])
    c1.markdown(f"`data/processed/{f.name}`")
    c2.download_button("Download", f.read_bytes(), file_name=f.name, mime="text/csv", key=f.name)

st.markdown("### Rebuild everything")
st.code(
    "python scripts/fetch_sources.py   # live mode: re-download the source samples\n"
    "python scripts/build_all.py       # offline mode: regenerate data/processed/ from the samples\n"
    "python scripts/check_package.py   # check the data package, docs and app against the rubric",
    language="bash",
)
