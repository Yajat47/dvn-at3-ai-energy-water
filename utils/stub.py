"""Placeholder shown on pages that are still being built. Delete the call once your page is real."""

import streamlit as st

from utils.story import PERSONA, TEAM


def coming_soon(*, key: str, title: str, need: int, brief: str, sources: list[tuple[str, str]]) -> None:
    st.title(title)
    st.caption(f"Page owner: {TEAM[key]} · Answers {PERSONA['name']}'s question: \"{PERSONA['needs'][need]}\"")
    st.info("This page is being built.", icon=":material/construction:")
    st.markdown(f"**Brief:** {brief}")
    st.markdown("**Where to start**")
    st.markdown("\n".join(f"- [{name}]({url})" for name, url in sources))
    with st.expander("Checklist for the page owner"):
        st.markdown(
            "- Copy `views/_page_template.py` into this file and build from there.\n"
            "- Put downloads in `data/raw/` and never edit them. Copy numbers taken from report text into "
            "`data/raw/manual/` with the original sentence in a `quote` column.\n"
            "- Write a `scripts/build_<page>.py` that produces your `data/processed/` files.\n"
            "- Add one row per source to `sources.csv`.\n"
            "- Put a `trace(...)` box under every chart.\n"
            "- Use colours from `utils/theme.py`. No dual axes, no pies for close values.\n"
            "- Add your design decision to `docs/design-log.md`.\n"
            "- Update your line in `STATUS` in `utils/story.py`."
        )
