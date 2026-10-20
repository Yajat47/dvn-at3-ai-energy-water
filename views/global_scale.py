"""1. Global scale: how big is the data-centre load, and how fast is it growing?

Owner: Yajat. Data built by scripts/build_global.py.
"""

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from utils import data
from utils.story import PERSONA, TEAM
from utils.theme import CONTEXT, INK, INK_2, PLOTLY_CONFIG, SERIES, SURFACE, style
from utils.trace import trace

RAW_SHARE = "data/raw/owid_data_centers_share_electricity_demand.csv"
RAW_DEMAND = "data/raw/owid_ember_electricity_demand.csv"
RAW_IEA = "data/raw/manual/iea_2026_key_questions.csv"
PROC_GLOBAL = "data/processed/global_dc_electricity.csv"
PROC_INDEX = "data/processed/global_growth_index.csv"
PROC_COMPARE = "data/processed/global_comparisons.csv"

ALL_YEARS = list(range(2020, 2026))  # IEA publishes 2020 and 2023-2025; 2021-22 stay empty


def gap_bridge(fig: go.Figure, series: pd.Series, color: str) -> None:
    """Faint solid join from 2020 to 2023, so the missing 2021-22 years read as 'no data', not as values."""
    fig.add_trace(go.Scatter(
        x=[2020, 2023], y=[series.loc[2020], series.loc[2023]], mode="lines", showlegend=False, hoverinfo="skip",
        line=dict(color=color, width=2), opacity=0.3,
    ))

# ---------------------------------------------------------------- data
g = data.processed("global_dc_electricity")
idx = data.processed("global_growth_index")
compare = data.processed("global_comparisons").set_index("entity")

world = g[(g["entity"] == "World") & (g["kind"] == "actual")].set_index("year")
proj = g[(g["entity"] == "World") & (g["kind"] == "projection")].iloc[0]
w25, w24, w20 = world.loc[2025], world.loc[2024], world.loc[2020]

yoy_growth = (w25["dc_twh"] / w24["dc_twh"] - 1) * 100
share_change = w25["dc_share_pct"] - w20["dc_share_pct"]
dc_index_25 = idx.query("year == 2025 and series == 'Data-centre electricity'")["index_2020"].item()
all_index_25 = idx.query("year == 2025 and series == 'All electricity demand'")["index_2020"].item()
dc_growth_20, all_growth_20 = dc_index_25 - 100, all_index_25 - 100
australia = compare.loc["Australia"]
france = compare.loc["France"]

# ---------------------------------------------------------------- header
st.title("1. Global scale")
st.subheader("A small slice of the world's electricity, growing fast")
st.caption(f"Page owner: {TEAM['global']} · Answers {PERSONA['name']}'s question: \"{PERSONA['needs'][0]}\"")

st.markdown(
    f"In 2025 the world's data centres used **{w25['dc_twh']:.0f} TWh** of electricity, "
    f"**{w25['dc_share_pct']:.1f}%** of all the electricity the world used. That is slightly more than "
    f"France's entire electricity demand and **{australia['ratio_dc_to_country']:.1f} times** Australia's. "
    f"It is still a small share, but it grew **{yoy_growth:.0f}%** in one year."
)

k1, k2, k3, k4 = st.columns(4)
k1.metric("Data-centre use, 2025", f"{w25['dc_twh']:.0f} TWh", f"+{yoy_growth:.0f}% on 2024",
          delta_color="off", border=True, help="IEA estimate, via Our World in Data")
k2.metric("World share, 2025", f"{w25['dc_share_pct']:.1f}%",
          f"+{share_change:.1f} pts since 2020", delta_color="off", border=True,
          help="IEA data-centre TWh divided by Ember world electricity demand")
k3.metric("Growth since 2020", f"+{dc_growth_20:.0f}%", f"All electricity: +{all_growth_20:.0f}%",
          delta_color="off", border=True, help="2020 to 2025, both in TWh")
k4.metric("IEA projection, 2030", f"{proj['dc_twh']:.0f} TWh", f"About {proj['dc_share_pct']:.0f}% of world electricity",
          delta_color="off", border=True, help="IEA 2026 base case")

# ---------------------------------------------------------------- chart 1: trajectory
st.markdown("#### Data-centre electricity use, 2020 to 2030")
measure = st.segmented_control(
    "Show as", ["Terawatt-hours", "Share of world electricity"], default="Terawatt-hours", key="global_measure"
)
as_share = measure == "Share of world electricity"
col, unit, fmt = ("dc_share_pct", "%", ".1f") if as_share else ("dc_twh", " TWh", ".0f")

actual = world[col].reindex(ALL_YEARS)  # NaN for 2021-22 breaks the line instead of inventing values
fig = go.Figure()
gap_bridge(fig, actual, SERIES[0])
fig.add_trace(go.Scatter(
    x=ALL_YEARS, y=actual, name="IEA estimate", mode="lines+markers", connectgaps=False,
    line=dict(color=SERIES[0], width=2.5),
    marker=dict(size=9, color=SERIES[0], line=dict(color=SURFACE, width=2)),
    hovertemplate=f"%{{y:{fmt}}}{unit}<extra>IEA estimate</extra>",
))
fig.add_trace(go.Scatter(
    x=[2025, 2030], y=[w25[col], proj[col]], name="IEA projection (base case)", mode="lines+markers",
    line=dict(color=SERIES[0], width=2, dash="dash"),
    marker=dict(size=[0, 9], color=SURFACE, line=dict(color=SERIES[0], width=2)),
    hovertemplate=f"%{{y:{fmt}}}{unit}<extra>IEA projection</extra>",
))
for x, y, text in [(2025, w25[col], f"<b>{w25[col]:{fmt}}{unit}</b> in 2025"),
                   (2030, proj[col], f"<b>{'~' if as_share else ''}{proj[col]:.0f}{unit}</b> projected")]:
    fig.add_annotation(x=x, y=y, text=text, showarrow=False, xanchor="right", yanchor="bottom",
                       xshift=-8, yshift=8, font=dict(color=INK, size=13))
if not as_share:
    fig.add_hline(y=australia["demand_twh"], line=dict(color=CONTEXT, width=1.5))
    fig.add_annotation(x=2030, y=australia["demand_twh"], xanchor="right", yanchor="bottom", showarrow=False,
                       text=f"All of Australia's electricity demand, 2025 ({australia['demand_twh']:.0f} TWh)",
                       font=dict(color=INK_2, size=12))
style(fig, y_title="% of world electricity" if as_share else "TWh per year")
fig.update_xaxes(dtick=1, range=[2019.6, 2030.4])
st.plotly_chart(fig, config=PLOTLY_CONFIG, width="stretch")
st.caption(
    "Solid line: IEA estimates. Dashed line: IEA 2026 base-case projection. The IEA publishes only the 2030 end "
    "point, so the dashes are a straight join between two published numbers, not a year-by-year forecast. "
    "The IEA published no estimates for 2021 and 2022, so that stretch is drawn faint: it joins two real points "
    "and carries no data of its own."
)

share_raw = data.raw("owid_data_centers_share_electricity_demand.csv")
demand_raw = data.raw("owid_ember_electricity_demand.csv")
iea_raw = data.raw("manual/iea_2026_key_questions.csv")
raw_share_world = share_raw[share_raw["Entity"] == "World"]
raw_demand_world = demand_raw[(demand_raw["Entity"] == "World") & (demand_raw["Year"] >= 2020)]
s25 = raw_share_world.set_index("Year").loc[2025].iloc[-1]
d25 = raw_demand_world.set_index("Year").loc[2025].iloc[-1]
trace(
    sources=["OWID-DC-SHARE", "OWID-EMBER-DEMAND", "IEA-2026-KQ"],
    files=[RAW_SHARE, RAW_DEMAND, RAW_IEA, PROC_GLOBAL, "scripts/build_global.py"],
    steps=[
        "Kept the World rows from the data-centre share file and the electricity demand file.",
        "Joined them on year. Only 2020 and 2023-2025 have both values.",
        "Data-centre TWh = share (%) / 100 x world electricity demand (TWh).",
        "Checked the 2025 result against the IEA report text (485 TWh). The build script stops if they differ by 2 TWh or more.",
        "Took the 2030 point (950 TWh, about 3%) from the IEA report text, stored word for word in the manual file.",
    ],
    worked_example=(
        f"World data-centre share, 2025 (raw file)   {s25:.7f} %\n"
        f"World electricity demand, 2025 (raw file)  {d25:,.2f} TWh\n"
        f"Data-centre electricity                    {s25:.7f} / 100 x {d25:,.2f} = {s25 / 100 * d25:.1f} TWh\n"
        f"IEA report text                            \"from 485 TWh in 2025 to 950 TWh in 2030\""
    ),
    tables={
        "Raw rows: data-centre share, World": raw_share_world,
        "Raw rows: electricity demand, World, 2020 onward": raw_demand_world,
        "Raw rows: IEA report numbers": iea_raw,
        "Processed rows used in this chart": g[g["entity"] == "World"],
    },
)

# ---------------------------------------------------------------- chart 2: growth vs all electricity
ratio = dc_growth_20 / all_growth_20
st.markdown(f"#### Data-centre demand grew about {ratio:.0f} times faster than electricity demand overall")
fig2 = go.Figure()
for series, color, width in [("Data-centre electricity", SERIES[0], 2.5), ("All electricity demand", CONTEXT, 2.5)]:
    s = idx[idx["series"] == series].set_index("year")["index_2020"].reindex(ALL_YEARS)
    gap_bridge(fig2, s, color)
    fig2.add_trace(go.Scatter(
        x=ALL_YEARS, y=s, name=series, mode="lines+markers", connectgaps=False,
        line=dict(color=color, width=width), marker=dict(size=8, color=color, line=dict(color=SURFACE, width=2)),
        hovertemplate="%{y:.0f}<extra>" + series + "</extra>",
    ))
    fig2.add_annotation(x=2025, y=s.loc[2025], text=f"<b>+{s.loc[2025] - 100:.0f}%</b> {series.lower()}",
                        showarrow=False, xanchor="left", xshift=10, font=dict(color=INK, size=13))
fig2.add_hline(y=100, line=dict(color=CONTEXT, width=1))
style(fig2, height=360, y_title="Index, 2020 = 100")
fig2.update_yaxes(rangemode="normal", range=[90, 195])
fig2.update_xaxes(dtick=1, range=[2019.7, 2027.2])
st.plotly_chart(fig2, config=PLOTLY_CONFIG, width="stretch")
st.caption("Both series start at 100 in 2020, so the gap shows the difference in growth rates, not in size.")
trace(
    sources=["OWID-DC-SHARE", "OWID-EMBER-DEMAND"],
    files=[PROC_GLOBAL, PROC_INDEX, "scripts/build_global.py"],
    steps=[
        "Took World data-centre TWh and World electricity demand TWh from the processed table above.",
        "Index = value in year / value in 2020 x 100, for each series separately.",
    ],
    worked_example=(
        f"Data centres:    {w25['dc_twh']:.0f} / {w20['dc_twh']:.0f} x 100 = {dc_index_25:.1f}  (+{dc_growth_20:.0f}%)\n"
        f"All electricity: {w25['demand_twh']:,.2f} / {w20['demand_twh']:,.2f} x 100 = {all_index_25:.1f}  "
        f"(+{all_growth_20:.0f}%)"
    ),
    tables={"Processed rows": idx},
)

# ---------------------------------------------------------------- chart 3: who uses it
regions = g[(g["kind"] == "actual") & (g["entity"] != "World")]
us_cn_share = (
    regions.query("year == 2025 and entity in ['United States', 'China']")["dc_twh"].sum() / w25["dc_twh"] * 100
)
st.markdown(f"#### Two countries use {us_cn_share:.0f}% of it")
fig3 = go.Figure()
for entity, color in [("United States", SERIES[0]), ("China", SERIES[1]), ("Rest of world", CONTEXT)]:
    r = regions[regions["entity"] == entity].sort_values("year")
    fig3.add_trace(go.Bar(
        x=r["year"].astype(str), y=r["dc_twh"], name=entity, marker=dict(color=color, line=dict(color="white", width=2)),
        text=[f"{v:.0f}" if y == 2025 else "" for y, v in zip(r["year"], r["dc_twh"])],
        textposition="inside", insidetextanchor="middle", textfont=dict(color="white", size=13),
        hovertemplate="%{y:.0f} TWh<extra>" + entity + "</extra>",
    ))
style(fig3, height=380, y_title="TWh per year")
fig3.update_layout(barmode="stack", bargap=0.45)
fig3.update_xaxes(type="category")
st.plotly_chart(fig3, config=PLOTLY_CONFIG, width="stretch")
st.caption("Labels show 2025 values in TWh. The years are the ones the IEA publishes.")
trace(
    sources=["OWID-DC-SHARE", "OWID-EMBER-DEMAND"],
    files=[RAW_SHARE, RAW_DEMAND, PROC_GLOBAL, "scripts/build_global.py"],
    steps=[
        "United States and China: data-centre share (%) / 100 x that country's electricity demand (TWh).",
        "Rest of world = World minus United States minus China, for each year.",
        "Two-country share = (United States + China) / World, 2025.",
    ],
    tables={"Processed rows": regions.pivot(index="year", columns="entity", values="dc_twh").reset_index()},
)

# ---------------------------------------------------------------- takeaway + bridge
with st.container(border=True):
    st.markdown(f"**What this means for {PERSONA['name']}**")
    st.markdown(
        f"Globally, data centres are a modest but fast-growing load: {w25['dc_share_pct']:.1f}% of world "
        f"electricity now, about {proj['dc_share_pct']:.0f}% by 2030 on the IEA's base case. On its own that is "
        f"not a reason for alarm. But {us_cn_share:.0f}% of the load sits in two countries, so in some local "
        "grids the share must be far above the global average. That is the question for Western Sydney."
    )
st.page_link("views/where_it_lands.py", label="Next: 2. Where it lands", icon=":material/arrow_forward:")

with st.expander("Design notes: why these charts"):
    st.markdown(
        "- **Line with a dashed projection, not a donut.** The visual task is change over time: how fast the "
        "share is moving toward the 2030 projection. A donut shows one year as a thin 1.5% sliver, cannot "
        "show the trend, and asks readers to compare angles, which people judge poorly.\n"
        "- **2021-22 drawn faint.** The IEA has no estimate for those years. A full-strength line from 2020 "
        "to 2023 would look like data we do not have; leaving it out would strand the 2020 point. A faint "
        "join keeps the shape readable and is honest about the gap.\n"
        "- **Growth chart indexed to 2020 = 100, not two y-axes.** Data-centre TWh and world TWh differ "
        "about 65-fold in size. A dual-axis chart lets the designer line the two up however they like, which "
        "invents a relationship. One indexed axis compares growth rates honestly.\n"
        "- **Australia reference line.** It gives the persona a yardstick she already knows.\n"
        "- **Colour.** One blue for the series that matters and grey for context; US and China get the first "
        "two palette colours, checked for colour-blind separation."
    )
