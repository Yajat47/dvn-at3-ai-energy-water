"""4. Water: company-reported data-centre water use, and why it is a local question.

Owner: Member C. Data built by scripts/build_water.py.
"""

import plotly.graph_objects as go
import streamlit as st

from utils import data
from utils.story import PERSONA
from utils.theme import CONTEXT, INK, PLOTLY_CONFIG, SERIES, SURFACE, style
from utils.trace import trace

RAW = "data/samples/manual/google_2026_water.csv"
PROC = "data/processed/water_google.csv"

w = data.processed("water_google").set_index("metric")
total = w.loc["water_consumption_total", "value"]
growth = w.loc["water_consumption_growth", "value"]
dalles = w.loc["water_consumption_the_dalles", "value"]
replenished = w.loc["water_replenished_total", "value"]
repl_share = w.loc["water_replenished_share_of_freshwater", "value"]
dalles_share = dalles / total * 100
year = int(w.loc["water_consumption_total", "year"])

st.title("4. Water")
st.subheader("The footprint is small in total, but it lands on one catchment at a time")
st.caption(f"Answers {PERSONA['name']}'s question: how heavily could a cluster load the local catchment?")

st.markdown(
    f"In {year} Google reports consuming **{total:.1f} billion gallons** of water across its data centres and "
    f"offices, up **{growth:.0f}%** on 2024. One site area, The Dalles in Oregon, accounts for "
    f"**{dalles * 1000:.0f} million gallons**, about **{dalles_share:.0f}%** of that total, in a single local "
    "water system. This is one company's report, not an industry total."
)

k1, k2, k3 = st.columns(3)
k1.metric(f"Total consumed, {year}", f"{total:.1f} bn gal", f"+{growth:.0f}% on 2024", delta_color="off", border=True)
k2.metric("Replenished", f"{replenished:.1f} bn gal", f"Reported as {repl_share:.0f}% of freshwater use",
          delta_color="off", border=True, help="The 78% uses Google's freshwater consumption as its base, "
          "not the total, so it is not 7.7 / 10.9.")
k3.metric("The Dalles share of total", f"{dalles_share:.1f}%", f"{dalles * 1000:.0f} million gallons",
          delta_color="off", border=True)

st.markdown(f"#### One site area is {dalles_share:.0f}% of Google's reported water use")
labels = ["Google total consumed", "Replenished by projects", "The Dalles, Oregon consumed"]
values = [total, replenished, dalles]
fig = go.Figure(go.Bar(
    x=labels, y=values, name=f"Google, {year}",
    marker=dict(color=[SERIES[0], CONTEXT, SERIES[1]], line=dict(color=SURFACE, width=2)),
    text=[f"{v:.1f}" if v >= 1 else f"{v:.3f}" for v in values], textposition="outside",
    textfont=dict(color=INK, size=13),
    hovertemplate="%{y:.3f} billion gallons<extra></extra>",
))
style(fig, height=400, x_title="Measure", y_title="Water (billion US gallons)",
      legend_title=f"Google-reported water, {year} (billion US gallons)")
fig.update_yaxes(range=[0, total * 1.2])
st.plotly_chart(fig, config=PLOTLY_CONFIG, width="stretch")
st.caption(
    f"Billion US gallons, calendar year {year}. Source: Google 2026 Environmental Report, pages 35 to 37. "
    "Company-reported, all sites combined except The Dalles. Replenished water is reported against freshwater "
    "consumption, not total consumption."
)

raw = data.sample("manual/google_2026_water.csv")
trace(
    sources=["GOOGLE-2026-ENV"],
    files=[RAW, PROC, "scripts/build_water.py"],
    steps=[
        "Copied five numbers from the Google 2026 Environmental Report into the manual file, with the page and a short phrase beside each.",
        "build_water.py keeps those rows and adds a plain-English label. No numbers are changed.",
        "The page computes the Dalles share = The Dalles gallons / total gallons x 100.",
    ],
    worked_example=(
        f"The Dalles consumption, {year} (raw file)  {dalles:.3f} billion gallons (469 million)\n"
        f"Google total consumption, {year} (raw file) {total:.1f} billion gallons\n"
        f"Share                                       {dalles:.3f} / {total:.1f} x 100 = {dalles_share:.1f}%"
    ),
    exact_rows=[
        ("The Dalles consumption", RAW, "water_consumption_the_dalles,2025,"),
        ("Google total consumption", RAW, "water_consumption_total,2025,"),
    ],
    tables={"Raw rows: Google report numbers": raw, "Processed rows used in this chart": w.reset_index()},
)

with st.container(border=True):
    st.markdown(f"**What this means for {PERSONA['name']}**")
    st.markdown(
        f"Google's report says data centres' combined water use is fairly small, but that it can still affect "
        f"local watersheds. What matters for {PERSONA['name']} is the local picture: a single site area was "
        f"{dalles_share:.0f}% of Google's use, and the report says water stress differs by catchment. So he should "
        "ask each applicant for site-level water use and cooling design, and check the local catchment's "
        "stress before treating a global figure as a local answer."
    )

with st.expander("Design notes: why this chart"):
    st.markdown(
        "- **Labelled bars, not a pie.** The visual task is comparing three quantities of very different size. "
        "Bars with labels let readers compare lengths and read exact values; a pie would show The Dalles as a "
        "thin sliver and hide the replenished comparison.\n"
        "- **One axis, one unit.** Billion US gallons throughout, so no dual axis and no invented relationship.\n"
        "- **Reported 78% kept separate.** It uses a different base (freshwater), so the page shows it as "
        "reported and never recomputes it.\n"
        "- **Company-reported caveat on screen.** The figures are Google's own."
    )
