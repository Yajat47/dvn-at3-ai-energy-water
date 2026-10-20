"""Sources and method. Owner: Yajat. Reads everything from data/data_dictionary.yml."""

import pandas as pd
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

st.markdown("### Sources")
st.dataframe(
    data.sources()[["id", "publisher", "title", "url", "licence", "retrieved"]],
    hide_index=True,
    width="stretch",
    column_config={"url": st.column_config.LinkColumn("url", display_text="open")},
)

st.markdown("### Datasets")
ds = data.datasets()
st.dataframe(
    pd.DataFrame(
        {
            "file": ds["path"],
            "role": ds["role"],
            "primary key": ds["primary_key"].map(", ".join),
            "time coverage": ds["time_coverage"].astype(str),
            "latest observation": ds["latest_observation"].astype(str),
            "made by": ds["transform"].map(lambda t: t if isinstance(t, str) else t["script"]),
        }
    ),
    hide_index=True,
    width="stretch",
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
