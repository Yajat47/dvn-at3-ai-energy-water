"""Home: the question, the persona and the story so far. Owner: Yajat."""

import streamlit as st

from utils import data
from utils.story import PERSONA, QUESTION, STATUS, TEAM, WHY_ARGUABLE
from utils.trace import trace

g = data.processed("global_dc_electricity")
compare = data.processed("global_comparisons").set_index("entity")
world = g[(g["entity"] == "World") & (g["kind"] == "actual")].set_index("year")
proj = g[(g["entity"] == "World") & (g["kind"] == "projection")].iloc[0]
w25, w24 = world.loc[2025], world.loc[2024]
yoy = (w25["dc_twh"] / w24["dc_twh"] - 1) * 100

st.title("AI's energy and water footprint")
st.markdown(f"### Our question: {QUESTION}")
st.markdown(WHY_ARGUABLE)

story, persona = st.columns([3, 2], gap="large")

with persona:
    with st.container(border=True):
        st.markdown(f"### {PERSONA['name']}")
        st.markdown(f"**{PERSONA['role']}**  \n_{PERSONA['note']}_")
        st.markdown(PERSONA["decision"])
        st.markdown("**What he needs to know**")
        st.markdown("\n".join(f"{i}. {q}" for i, q in enumerate(PERSONA["needs"], start=1)))

with story:
    st.markdown("### The story so far")

    with st.container(border=True):
        st.markdown(f"**1. Global scale** · {TEAM['global']} · _{STATUS['global']}_")
        st.markdown(
            f"Data centres used **{w25['dc_twh']:.0f} TWh** in 2025, **{w25['dc_share_pct']:.1f}%** of world "
            f"electricity and slightly more than all of France. That was up {yoy:.0f}% in a year. The IEA expects "
            f"**{proj['dc_twh']:.0f} TWh** (about {proj['dc_share_pct']:.0f}%) by 2030."
        )
        st.page_link("views/global_scale.py", label="Open page 1", icon=":material/arrow_forward:")

    with st.container(border=True):
        st.markdown(f"**2. Where it lands** · {TEAM['where']} · _{STATUS['where']}_")
        st.markdown(
            "How large is the data-centre share of the grids it actually connects to? Covers Ireland, "
            "US hubs and Australia's National Electricity Market, with NSW highlighted."
        )
        st.page_link("views/where_it_lands.py", label="Open page 2", icon=":material/arrow_forward:")

    with st.container(border=True):
        st.markdown(f"**3. Compute vs efficiency** · {TEAM['compute']} · _{STATUS['compute']}_")
        st.markdown("Is efficiency improving fast enough to offset the growth in AI compute?")
        st.page_link("views/compute_vs_efficiency.py", label="Open page 3", icon=":material/arrow_forward:")

    with st.container(border=True):
        st.markdown(f"**4. Water** · {TEAM['water']} · _{STATUS['water']}_")
        st.markdown("What does the boom mean for water, the second meter that gets far less attention?")
        st.page_link("views/water.py", label="Open page 4", icon=":material/arrow_forward:")

    with st.container(border=True):
        st.markdown("**Verdict** · _draft, finalised once all four pages are in_")
        st.markdown(
            "Working hypothesis: small and manageable globally, significant locally. Whether that holds for "
            "Western Sydney depends on pages 2 and 4."
        )

trace(
    sources=["OWID-DC-SHARE", "OWID-EMBER-DEMAND", "IEA-2026-KQ"],
    files=["data/processed/global_dc_electricity.csv", "data/processed/global_comparisons.csv"],
    steps=[
        "Numbers in card 1 come from page 1's processed tables. Open page 1 for the full trace.",
        "Growth = 2025 TWh / 2024 TWh - 1.",
        "France comparison: France's 2025 electricity demand from the same Ember file.",
    ],
    tables={"2025 comparison with whole countries": compare.reset_index()},
)

st.caption("Every chart in this app has a box like the one above showing the source file and every step applied.")
