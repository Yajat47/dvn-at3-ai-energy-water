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
            "Full list: `docs/PART2_CHECKLIST.md`.\n\n"
            "- Copy `views/_page_template.py` into this file and build from there.\n"
            "- Put source files in `data/samples/` unchanged; numbers from report text go in "
            "`data/samples/manual/` with the original sentence in a `quote` column.\n"
            "- Write `scripts/build_<page>.py` to produce your `data/processed/` files.\n"
            "- Describe every file in `data/data_dictionary.yml`.\n"
            "- Each chart: finding as title, caption with unit, baseline and years, axis and legend titles, "
            "labelled values, and a `trace(...)` box.\n"
            "- Add your limits to `LIMITS` in `utils/story.py`.\n"
            "- Add your row to `docs/AI_PROVENANCE.md` and your section to `DISCLOSURE.md`.\n"
            "- Run `python scripts/build_all.py` and `python scripts/check_package.py` before your PR."
        )
