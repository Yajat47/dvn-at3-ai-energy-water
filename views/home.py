"""Home: the question, a headline fact about the whole dataset, the answer, and the limits. Owner: Yajat."""

import streamlit as st

from utils import data
from utils.story import LIMITS, PERSONA, QUESTION, STATUS, TEAM, USER_STORIES, WHY_ARGUABLE
from utils.trace import trace

g = data.processed("global_dc_electricity")
compare = data.processed("global_comparisons").set_index("entity")
actual = g[g["kind"] == "actual"]
world = actual[actual["entity"] == "World"].set_index("year")
us = actual[actual["entity"] == "United States"].set_index("year")
proj = g[(g["entity"] == "World") & (g["kind"] == "projection")].iloc[0]
w25, w24 = world.loc[2025], world.loc[2024]
us25 = us.loc[2025]
yoy = (w25["dc_twh"] / w24["dc_twh"] - 1) * 100
us_cn = actual.query("year == 2025 and entity in ['United States', 'China']")["dc_twh"].sum()
us_cn_pct = us_cn / w25["dc_twh"] * 100
us_vs_world = us25["dc_share_pct"] / w25["dc_share_pct"]

# ---------------------------------------------------------------- opening screen
st.title("AI's energy and water footprint")
st.markdown(f"### Our question: {QUESTION}")

with st.container(border=True):
    st.markdown("**Across the whole dataset, in 2025**")
    m1, m2, m3 = st.columns(3)
    m1.metric("World data-centre electricity", f"{w25['dc_twh']:.0f} TWh")
    m2.metric("Share of world electricity", f"{w25['dc_share_pct']:.1f}%")
    m3.metric("Share of US electricity", f"{us25['dc_share_pct']:.1f}%")
    st.caption("IEA estimates via Our World in Data; shares are data-centre TWh divided by total electricity "
               "demand (Ember). Calendar year 2025.")

st.markdown(WHY_ARGUABLE)

# ---------------------------------------------------------------- answer
st.markdown("## Our answer")
st.markdown(
    f"**More a local problem than a global one.** Measured against the world, data centres are a small load: "
    f"{w25['dc_share_pct']:.1f}% of electricity in 2025, heading for about {proj['dc_share_pct']:.0f}% by 2030 on "
    f"the IEA's base case. But the load is concentrated. The United States and China used {us_cn_pct:.0f}% of the "
    f"world's data-centre electricity in 2025, and in the United States data centres took {us25['dc_share_pct']:.1f}% "
    f"of all electricity, {us_vs_world:.1f} times the world share. That concentration is what turns a small global "
    f"number into a local planning question for {PERSONA['name']}."
)
# TEAM: extend this answer with the local evidence from pages 2 and 4 once they are final.

# ---------------------------------------------------------------- persona + stories
left, right = st.columns([3, 2], gap="large")
with right:
    with st.container(border=True):
        st.markdown(f"### {PERSONA['name']}")
        st.markdown(f"**{PERSONA['role']}**  \n_{PERSONA['note']}_")
        st.markdown(PERSONA["decision"])

with left:
    st.markdown(f"### What {PERSONA['name']} can do here")
    for i, s in enumerate(USER_STORIES, start=1):
        with st.container(border=True):
            st.markdown(f"**{i}.** As an {s['as_a']}, I want {s['i_want']}, so that {s['so_that']}.")
            cols = st.columns(len(s["pages"]))
            for col, page in zip(cols, s["pages"]):
                col.page_link(page, icon=":material/arrow_forward:")

st.markdown("### Pages")
cards = [
    ("1. Global scale", "global", "views/global_scale.py"),
    ("2. Where it lands", "where", "views/where_it_lands.py"),
    ("3. Compute vs efficiency", "compute", "views/compute_vs_efficiency.py"),
    ("4. Water", "water", "views/water.py"),
]
for col, (title, key, page) in zip(st.columns(4), cards):
    with col.container(border=True):
        st.markdown(f"**{title}**  \n{TEAM[key]} · _{STATUS[key]}_")
        st.page_link(page, label="Open", icon=":material/arrow_forward:")

# ---------------------------------------------------------------- limits
st.markdown("## What this data cannot show")
st.markdown("\n".join(f"- {limit}" for limit in LIMITS))

trace(
    sources=["OWID-DC-SHARE", "OWID-EMBER-DEMAND", "IEA-2026-KQ"],
    files=["data/processed/global_dc_electricity.csv", "data/processed/global_comparisons.csv"],
    steps=[
        "Opening figures and the answer use the 2025 rows of global_dc_electricity (World, United States, China).",
        "US and China share of world data-centre electricity = (US TWh + China TWh) / World TWh, 2025.",
        "US share vs world share = US data-centre share / world data-centre share, 2025.",
        "2030 share is the IEA 2026 base-case projection.",
    ],
    worked_example=(
        f"US + China, 2025:   {us_cn:.0f} TWh / {w25['dc_twh']:.0f} TWh = {us_cn_pct:.1f}%\n"
        f"US vs world share:  {us25['dc_share_pct']:.2f}% / {w25['dc_share_pct']:.2f}% = {us_vs_world:.2f}x\n"
        f"World growth:       {w25['dc_twh']:.0f} / {w24['dc_twh']:.0f} - 1 = {yoy:.1f}%"
    ),
    tables={"2025 rows used": actual[actual["year"] == 2025]},
)
