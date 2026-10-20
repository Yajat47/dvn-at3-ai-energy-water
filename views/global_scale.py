"""1. Global scale: how big is the data-centre load, and how fast is it growing?

Owner: Yajat. Data built by scripts/build_global.py.
"""

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from utils import data
from utils.story import PERSONA, TEAM
from utils.theme import CONTEXT, INK, INK_2, PLOTLY_CONFIG, SERIES, SURFACE, style
from utils.trace import line_number, trace

RAW_SHARE = "data/samples/owid_data_centers_share_electricity_demand.csv"
RAW_DEMAND = "data/samples/owid_ember_electricity_demand.csv"
RAW_IEA = "data/samples/manual/iea_2026_key_questions.csv"
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
    f"France's entire electricity demand ({france['demand_twh']:.0f} TWh) and "
    f"**{australia['ratio_dc_to_country']:.1f} times** Australia's ({australia['demand_twh']:.0f} TWh). "
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
k4.metric("IEA projection, 2030", f"{proj['dc_twh']:.0f} TWh", f"~{proj['dc_share_pct']:.0f}% of world total",
          delta_color="off", border=True, help="IEA 2026 base case")
st.caption("World totals for calendar year 2025 unless stated. Growth compares TWh in 2025 with 2024 and with "
           "2020. Country comparisons use Ember 2025 electricity demand.")

# ---------------------------------------------------------------- chart 1: trajectory
st.markdown("#### Data-centre electricity use, 2020 to 2030")
measure = st.segmented_control(
    "Show as", ["Terawatt-hours", "Share of world electricity"], default="Terawatt-hours", key="global_measure"
)
as_share = measure == "Share of world electricity"
col, unit, fmt = ("dc_share_pct", "%", ".1f") if as_share else ("dc_twh", " TWh", ".0f")

actual = world[col].reindex(ALL_YEARS)  # NaN for 2021-22 breaks the line instead of inventing values
labels = [f"{v:{fmt}}{unit}" if pd.notna(v) else "" for v in actual]
fig = go.Figure()
gap_bridge(fig, actual, SERIES[0])
fig.add_trace(go.Scatter(
    x=ALL_YEARS, y=actual, name="IEA estimate", mode="lines+markers+text", connectgaps=False,
    text=labels, textposition=["top right" if y == 2020 else "top left" for y in ALL_YEARS],
    textfont=dict(color=INK, size=13),
    line=dict(color=SERIES[0], width=2.5),
    marker=dict(size=9, color=SERIES[0], line=dict(color=SURFACE, width=2)),
    hovertemplate=f"%{{y:{fmt}}}{unit}<extra>IEA estimate</extra>",
))
fig.add_trace(go.Scatter(
    x=[2025, 2030], y=[w25[col], proj[col]], name="IEA projection (base case)", mode="lines+markers+text",
    text=["", f"{'~' if as_share else ''}{proj[col]:.0f}{unit} (projection)"], textposition="top left",
    textfont=dict(color=INK, size=13),
    line=dict(color=SERIES[0], width=2, dash="dash"),
    marker=dict(size=[0, 9], color=SURFACE, line=dict(color=SERIES[0], width=2)),
    hovertemplate=f"%{{y:{fmt}}}{unit}<extra>IEA projection</extra>",
))
if not as_share:
    fig.add_hline(y=australia["demand_twh"], line=dict(color=CONTEXT, width=1.5))
    fig.add_annotation(x=2030, y=australia["demand_twh"], xanchor="right", yanchor="bottom", showarrow=False,
                       text=f"All of Australia's electricity demand, 2025 ({australia['demand_twh']:.0f} TWh)",
                       font=dict(color=INK_2, size=12))
y_label = "Share of world electricity demand (%)" if as_share else "Data-centre electricity (TWh per year)"
style(fig, x_title="Year", y_title=y_label,
      legend_title="Data-centre electricity, " + ("% of world demand" if as_share else "TWh per year"))
fig.update_xaxes(dtick=1, range=[2019.6, 2030.4])
fig.update_yaxes(range=[0, (proj[col] * 1.15)])
st.plotly_chart(fig, config=PLOTLY_CONFIG, width="stretch")
st.caption(
    f"World data-centre electricity in {'% of world electricity demand' if as_share else 'TWh per year'}. "
    "Solid line: IEA estimates for 2020 and 2023-2025. Dashed line: IEA 2026 base-case projection; the IEA "
    "publishes only the 2030 end point, so the dashes join two published numbers and are not a year-by-year "
    "forecast. There are no IEA estimates for 2021 and 2022, so that stretch is drawn faint and carries no data."
)

share_raw = data.sample("owid_data_centers_share_electricity_demand.csv")
demand_raw = data.sample("owid_ember_electricity_demand.csv")
iea_raw = data.sample("manual/iea_2026_key_questions.csv")
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
    exact_rows=[
        ("World data-centre share, 2025", RAW_SHARE, "World,OWID_WRL,2025,"),
        ("World electricity demand, 2025", RAW_DEMAND, "World,OWID_WRL,2025,"),
        ("IEA sentence with 485 TWh and 950 TWh", RAW_IEA, "data_centre_electricity,2025,"),
    ],
    tables={
        "The two raw rows behind 485 TWh": pd.DataFrame(
            [
                {"What": "World data-centre share, 2025", "File": RAW_SHARE.split("/")[-1],
                 "Line": str(line_number(RAW_SHARE, "World,OWID_WRL,2025,")), "Value": f"{s25:.7f} %"},
                {"What": "World electricity demand, 2025", "File": RAW_DEMAND.split("/")[-1],
                 "Line": str(line_number(RAW_DEMAND, "World,OWID_WRL,2025,")), "Value": f"{d25:,.2f} TWh"},
                {"What": "Share / 100 x demand", "File": "", "Line": "", "Value": f"{s25 / 100 * d25:.1f} TWh"},
            ]
        ),
        "Raw rows: IEA report numbers": iea_raw,
        "Raw rows: data-centre share, World": raw_share_world,
        "Raw rows: electricity demand, World, 2020 onward": raw_demand_world,
        "Processed rows used in this chart": g[g["entity"] == "World"],
    },
)

# ---------------------------------------------------------------- chart 2: growth vs all electricity
ratio = dc_growth_20 / all_growth_20
st.markdown(f"#### Data-centre demand grew about {ratio:.0f} times faster than electricity demand overall")
fig2 = go.Figure()
for series, color, pos in [("Data-centre electricity", SERIES[0], "top left"),
                           ("All electricity demand", CONTEXT, "bottom right")]:
    s_ = idx[idx["series"] == series].set_index("year")["index_2020"].reindex(ALL_YEARS)
    gap_bridge(fig2, s_, color)
    fig2.add_trace(go.Scatter(
        x=ALL_YEARS, y=s_, name=series, mode="lines+markers+text", connectgaps=False,
        text=[f"{v:.0f}" if pd.notna(v) else "" for v in s_],
        textposition=[pos.replace("left", "right") if y == 2020
                      else "bottom center" if (y == 2025 and pos.startswith("bottom")) else pos for y in ALL_YEARS],
        textfont=dict(color=INK, size=12),
        line=dict(color=color, width=2.5), marker=dict(size=8, color=color, line=dict(color=SURFACE, width=2)),
        hovertemplate="%{y:.0f}<extra>" + series + "</extra>",
    ))
    fig2.add_annotation(x=2025, y=s_.loc[2025], text=f"<b>+{s_.loc[2025] - 100:.0f}%</b> {series.lower()}",
                        showarrow=False, xanchor="left", xshift=14, font=dict(color=INK, size=13))
fig2.add_hline(y=100, line=dict(color=CONTEXT, width=1))
style(fig2, height=380, x_title="Year", y_title="Index (2020 = 100)", legend_title="World series, index (2020 = 100)")
fig2.update_yaxes(rangemode="normal", range=[85, 200])
fig2.update_xaxes(dtick=1, range=[2019.6, 2027.6])
st.plotly_chart(fig2, config=PLOTLY_CONFIG, width="stretch")
st.caption(
    "World data-centre electricity and world electricity demand, both indexed to 2020 = 100 and both measured "
    "in TWh. Years 2020 and 2023-2025. The gap shows the difference in growth rates, not in size: world demand "
    "is about 65 times larger."
)
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
us25 = regions[(regions["entity"] == "United States") & (regions["year"] == 2025)].iloc[0]
us_cn_share = (
    regions.query("year == 2025 and entity in ['United States', 'China']")["dc_twh"].sum() / w25["dc_twh"] * 100
)
st.markdown(f"#### Two countries use {us_cn_share:.0f}% of it")
REGION_COLOURS = {"United States": SERIES[0], "China": SERIES[1], "Rest of world": CONTEXT}
chosen = st.multiselect("Regions to show", list(REGION_COLOURS), default=list(REGION_COLOURS), key="global_regions")
if not chosen:
    st.info("No regions selected. Choose at least one region above to see its data-centre electricity.",
            icon=":material/filter_alt_off:")
else:
    fig3 = go.Figure()
    for entity in chosen:
        r = regions[regions["entity"] == entity].sort_values("year")
        fig3.add_trace(go.Bar(
            x=r["year"].astype(str), y=r["dc_twh"], name=entity,
            marker=dict(color=REGION_COLOURS[entity], line=dict(color="white", width=2)),
            text=[f"{v:.0f}" for v in r["dc_twh"]], textposition="inside", insidetextanchor="middle",
            textfont=dict(color="white", size=13),
            hovertemplate="%{y:.0f} TWh<extra>" + entity + "</extra>",
        ))
    totals = regions[regions["entity"].isin(chosen)].groupby("year")["dc_twh"].sum()
    # Totals as a text-only trace: annotations would read "2020" as a category position, not a label.
    fig3.add_trace(go.Scatter(
        x=[str(y) for y in totals.index], y=totals.values, mode="text", text=[f"<b>{v:.0f}</b>" for v in totals],
        textposition="top center", textfont=dict(color=INK, size=13), showlegend=False, hoverinfo="skip",
    ))
    style(fig3, height=400, x_title="Year", y_title="Data-centre electricity (TWh per year)",
          legend_title="Region (TWh per year)")
    fig3.update_layout(barmode="stack", bargap=0.45, uniformtext=dict(minsize=11, mode="show"))
    fig3.update_xaxes(type="category")
    fig3.update_yaxes(range=[0, totals.max() * 1.15])
    st.plotly_chart(fig3, config=PLOTLY_CONFIG, width="stretch")
    st.caption(
        "Data-centre electricity in TWh per year by region, for the years the IEA publishes (2020, 2023-2025). "
        "Numbers inside bars are each region's TWh; bold numbers on top are the total of the regions shown. "
        "Rest of world = World minus United States minus China."
    )
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
        f"not a reason for alarm. But {us_cn_share:.0f}% of the load sits in two countries, and in the United "
        f"States data centres already use {us25['dc_share_pct']:.1f}% of all electricity, "
        f"{us25['dc_share_pct'] / w25['dc_share_pct']:.1f} times the world share. Page 2 looks at where that "
        "concentrated load lands."
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
        "- **Australia reference line.** It gives the persona a yardstick he already knows.\n"
        "- **Colour.** One blue for the series that matters and grey for context; US and China get the first "
        "two palette colours, checked for colour-blind separation."
    )
