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

water = data.processed("water_google").set_index("metric")
water_year = int(water.loc["water_consumption_total", "year"])
water_total = water.loc["water_consumption_total", "value"]
water_growth = water.loc["water_consumption_growth", "value"]
dalles = water.loc["water_consumption_the_dalles", "value"]
dalles_share = dalles / water_total * 100

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
    "**More a local problem than a global one.** Measured against the world, data centres are a small load. "
    "But the load is concentrated, in electricity and in water:"
)
st.markdown(
    f"- **Global scale (page 1).** Data centres used {w25['dc_share_pct']:.1f}% of the world's electricity in 2025, "
    f"heading for about {proj['dc_share_pct']:.0f}% by 2030 on the IEA's base case. The United States and China used "
    f"{us_cn_pct:.0f}% of that data-centre electricity.\n"
    f"- **Where it lands (page 2).** In the United States, data centres took {us25['dc_share_pct']:.1f}% of all "
    f"electricity in 2025, {us_vs_world:.1f} times the world share.\n"
    f"- **Water (page 4).** Google reports consuming {water_total:.1f} billion gallons of water in {water_year}, up "
    f"{water_growth:.0f}% on {water_year - 1}. One site area, The Dalles in Oregon, accounted for "
    f"{dalles_share:.0f}% of it."
)
st.markdown(
    f"That concentration is what turns a small global number into a local planning question for {PERSONA['name']}. "
    "Our data stops at national electricity totals and one company's water report, so it shows the concentration "
    "but cannot measure the load on any single grid or catchment, Western Sydney's included."
)

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
    sources=["OWID-DC-SHARE", "OWID-EMBER-DEMAND", "IEA-2026-KQ", "GOOGLE-2026-ENV"],
    files=["data/processed/global_dc_electricity.csv", "data/processed/global_comparisons.csv",
           "data/processed/water_google.csv"],
    steps=[
        "Opening figures and the electricity points in the answer use the 2025 rows of global_dc_electricity "
        "(World, United States, China).",
        "US and China share of world data-centre electricity = (US TWh + China TWh) / World TWh, 2025.",
        "US share vs world share = US data-centre share / world data-centre share, 2025.",
        "2030 share is the IEA 2026 base-case projection.",
        "Water figures are Google's reported numbers in water_google, unchanged. "
        "The Dalles share = The Dalles gallons / total gallons x 100.",
    ],
    worked_example=(
        f"US + China, 2025:   {us_cn:.0f} TWh / {w25['dc_twh']:.0f} TWh = {us_cn_pct:.1f}%\n"
        f"US vs world share:  {us25['dc_share_pct']:.2f}% / {w25['dc_share_pct']:.2f}% = {us_vs_world:.2f}x\n"
        f"World growth:       {w25['dc_twh']:.0f} / {w24['dc_twh']:.0f} - 1 = {yoy:.1f}%\n"
        f"The Dalles share:   {dalles:.3f} / {water_total:.1f} billion gallons x 100 = {dalles_share:.1f}%"
    ),
    tables={"2025 rows used": actual[actual["year"] == 2025], "Water rows used": water.reset_index()},
)
