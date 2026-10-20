"""The "Where does this number come from?" box that sits under every chart.

Usage:
    trace(
        sources=["OWID-DC-SHARE"],
        files=["data/raw/owid_data_centers_share_electricity_demand.csv"],
        steps=["Kept World rows", "Multiplied share by demand"],
        tables={"Processed rows": df},
    )
"""

import pandas as pd
import streamlit as st

from utils.data import sources as load_sources

REPO_URL = "https://github.com/Yajat47/dvn-at3-ai-energy-water/blob/main/"


def trace(
    *,
    sources: list[str],
    files: list[str],
    steps: list[str],
    tables: dict[str, pd.DataFrame] | None = None,
    worked_example: str | None = None,
    label: str = "Where does this number come from?",
) -> None:
    with st.expander(label):
        registry = load_sources().set_index("source_id")
        st.markdown("**Sources**")
        for sid in sources:
            if sid in registry.index:
                row = registry.loc[sid]
                st.markdown(f"- `{sid}`: [{row['title']}]({row['url']}) ({row['publisher']}, retrieved {row['retrieved']})")
            else:
                st.markdown(f"- `{sid}`: missing from sources.csv, add it")

        st.markdown("**Files**")
        for f in files:
            st.markdown(f"- [`{f}`]({REPO_URL}{f})")

        st.markdown("**What we did**")
        st.markdown("\n".join(f"{i}. {s}" for i, s in enumerate(steps, start=1)))

        if worked_example:
            st.markdown("**Worked example**")
            st.code(worked_example, language=None)

        for name, df in (tables or {}).items():
            st.markdown(f"**{name}**")
            st.dataframe(df, hide_index=True, width="stretch")
