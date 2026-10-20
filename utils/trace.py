"""The "Where does this number come from?" box that sits under every chart.

Usage:
    trace(
        sources=["OWID-DC-SHARE"],
        files=["data/samples/owid_data_centers_share_electricity_demand.csv"],
        steps=["Kept World rows", "Multiplied share by demand"],
        exact_rows=[("World share, 2025", "data/samples/owid_data_centers_share_electricity_demand.csv",
                     "World,OWID_WRL,2025,")],
        tables={"Processed rows": df},
    )
"""

import pandas as pd
import streamlit as st

from utils.data import ROOT
from utils.data import sources as load_sources

REPO_URL = "https://github.com/Yajat47/dvn-at3-ai-energy-water/blob/main/"


@st.cache_data
def line_number(path: str, starts_with: str) -> int | None:
    """1-based line number of the first line in a repo file that starts with `starts_with`."""
    with open(ROOT / path, encoding="utf-8") as fh:
        for n, line in enumerate(fh, start=1):
            if line.startswith(starts_with):
                return n
    return None


def trace(
    *,
    sources: list[str],
    files: list[str],
    steps: list[str],
    tables: dict[str, pd.DataFrame] | None = None,
    worked_example: str | None = None,
    exact_rows: list[tuple[str, str, str]] | None = None,
    label: str = "Where does this number come from?",
) -> None:
    """exact_rows: (label, repo path, line prefix) -> a link that opens GitHub on that exact row."""
    with st.expander(label):
        registry = load_sources().set_index("id")
        st.markdown("**Sources**")
        for sid in sources:
            if sid in registry.index:
                row = registry.loc[sid]
                st.markdown(f"- `{sid}`: [{row['title']}]({row['url']}) ({row['publisher']}, retrieved {row['retrieved']})")
            else:
                st.markdown(f"- `{sid}`: missing from data/data_dictionary.yml, add it")

        st.markdown("**Files**")
        for f in files:
            st.markdown(f"- [`{f}`]({REPO_URL}{f})")

        if exact_rows:
            st.markdown("**Open the exact source row on GitHub**")
            for name, path, prefix in exact_rows:
                n = line_number(path, prefix)
                if n:
                    st.markdown(f"- [{name}: `{path}`, line {n}]({REPO_URL}{path}?plain=1#L{n})")

        st.markdown("**What we did**")
        st.markdown("\n".join(f"{i}. {s}" for i, s in enumerate(steps, start=1)))

        if worked_example:
            st.markdown("**Worked example**")
            st.code(worked_example, language=None)

        for name, df in (tables or {}).items():
            st.markdown(f"**{name}**")
            st.dataframe(df, hide_index=True, width="stretch")
