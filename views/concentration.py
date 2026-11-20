"""5. Concentration: who drives the compute? The concentration of frontier AI.

Owner: Sai Akarsh Viragani. Data built by scripts/build_concentration.py.
"""

import plotly.graph_objects as go
import streamlit as st

from utils import data
from utils.story import PERSONA, TEAM
from utils.theme import CONTEXT, INK, INK_2, PLOTLY_CONFIG, SERIES, SURFACE, style
from utils.trace import trace

KEY = "concentration"
RAW_MODELS = "data/samples/epoch_notable_ai_models.csv"
PROC_ORGS = "data/processed/compute_concentration_orgs.csv"
PROC_CNTRY = "data/processed/compute_concentration_countries.csv"

# ---------------------------------------------------------------- data
orgs = data.processed("compute_concentration_orgs")
countries = data.processed("compute_concentration_countries").set_index("country")

named_top4 = orgs[orgs["organization"].isin(["OpenAI", "xAI", "Meta AI", "Google DeepMind"])]
top4_share = named_top4["share_pct"].sum()
top2_share = orgs[orgs["organization"].isin(["OpenAI", "xAI"])]["share_pct"].sum()
top_org = orgs.iloc[0]
us_row = countries.loc["United States"]
china_row = countries.loc["China"]
row_row = countries.loc["Rest of world"]

st.title("5. Concentration")
st.subheader("Frontier AI compute is hyper-concentrated in a tiny handful of American hyperscalers")
st.caption(f"Page owner: {TEAM.get(KEY, 'Sai')} · Answers {PERSONA['name']}'s question: \"Who is actually driving the explosive compute demand?\"")

st.markdown(
    f"Across all notable AI models released since 2020, training compute is not spread evenly across "
    f"the tech industry. Just four organizations—**OpenAI**, **xAI**, **Meta AI**, and **Google DeepMind**—account "
    f"for **{top4_share:.1f}%** of all notable training compute. The top two alone account for **{top2_share:.1f}%**. "
    f"Geographically, the United States accounts for **{us_row['share_pct']:.1f}%** of all frontier compute, China "
    f"accounts for **{china_row['share_pct']:.1f}%**, and the rest of the world combined represents just **{row_row['share_pct']:.1f}%**."
)

k1, k2, k3 = st.columns(3)
k1.metric("Top 4 hyperscalers share", f"{top4_share:.1f}%", f"{top_org['organization']} alone: {top_org['share_pct']:.1f}%",
          delta_color="off", border=True, help="Combined compute share of OpenAI, xAI, Meta AI, and Google DeepMind since 2020")
k2.metric("United States share", f"{us_row['share_pct']:.1f}%", f"{us_row['models_count']} notable models",
          delta_color="off", border=True, help="Total training compute from organizations headquartered in the US")
k3.metric("Rest of world combined", f"{row_row['share_pct']:.1f}%", f"{row_row['models_count']} models globally",
          delta_color="off", border=True, help="All other countries combined outside the US and China")

st.caption("Figures cover notable AI models released 2020–2026 with documented training compute from Epoch AI.")

# ---------------------------------------------------------------- chart 1: organizational concentration
st.markdown(f"#### Just two organizations account for {top2_share:.0f}% of frontier AI training compute")

org_list = orgs["organization"].tolist()
chosen_orgs = st.multiselect("Organizations to show", org_list, default=org_list, key="conc_org_filter")

if not chosen_orgs:
    st.info("No organizations selected. Please choose at least one organization above to display compute shares.",
            icon=":material/filter_alt_off:")
else:
    filtered_orgs = orgs[orgs["organization"].isin(chosen_orgs)].sort_values("share_pct", ascending=True)
    
    # Colors match geography consistently across both charts:
    # Blue (SERIES[0]) for United States, Orange (SERIES[1]) for China, Grey (CONTEXT) for Rest of world
    bar_colors = [
        SERIES[1] if country == "China" else (SERIES[0] if country == "United States" else CONTEXT)
        for country in filtered_orgs["country"]
    ]
    
    fig1 = go.Figure(go.Bar(
        x=filtered_orgs["share_pct"],
        y=filtered_orgs["organization"],
        orientation="h",
        name="Compute share (%)",
        marker=dict(color=bar_colors, line=dict(color=SURFACE, width=1.5)),
        text=[f"{v:.1f}%" for v in filtered_orgs["share_pct"]],
        textposition="outside",
        textfont=dict(color=INK, size=12),
        hovertemplate="%{y}: %{x:.2f}% of post-2020 compute<extra></extra>",
    ))
    
    max_val = filtered_orgs["share_pct"].max()
    fig1.update_xaxes(range=[0, max_val * 1.25], ticksuffix="%")
    style(fig1, height=440, x_title="Share of notable training compute since 2020 (%)",
          y_title="Organization or group", legend=False)
    st.plotly_chart(fig1, config=PLOTLY_CONFIG, width="stretch")
    st.caption(
        "Share of total floating-point operations (FLOP) used to train notable models released 2020–2026. "
        "Source: Epoch AI Notable AI Models dataset. Values are labelled directly on each bar. "
        "Bar colors match geography across both charts: Blue for US organizations (summing to 90.6%), "
        "Orange for Chinese organizations (summing to 8.1%), and Grey for Rest of world (1.3%). "
        "Chart 2 below summarizes these exact national totals."
    )

raw_models_df = data.sample("epoch_notable_ai_models.csv")
trace(
    sources=["EPOCH-MODELS"],
    files=[RAW_MODELS, PROC_ORGS, "scripts/build_concentration.py"],
    steps=[
        "Filtered Epoch AI notable models to entries published from 2020 onwards with positive training compute (FLOP).",
        "Extracted the primary organization for each model and consolidated research labs under parent entities.",
        "Summed total training compute per organization and identified the top named entities.",
        "Aggregated remaining models by geographic origin (Other US, Other China, Rest of world).",
        "Computed each entity's share: entity FLOP / total post-2020 FLOP x 100.",
    ],
    worked_example=(
        f"Total post-2020 FLOP in dataset:       {orgs['total_compute_flop'].sum():.3e} FLOP\n"
        f"OpenAI training compute:               {top_org['total_compute_flop']:.3e} FLOP\n"
        f"OpenAI share:                          {top_org['total_compute_flop']:.3e} / {orgs['total_compute_flop'].sum():.3e} x 100 = {top_org['share_pct']:.2f}%\n"
        f"Top 4 US hyperscalers combined:        {named_top4['total_compute_flop'].sum():.3e} FLOP ({top4_share:.1f}%)\n"
        f"United States total (Chart 2):         {us_row['total_compute_flop']:.3e} FLOP ({us_row['share_pct']:.2f}%)\n"
        f"China total (Chart 2):                 {china_row['total_compute_flop']:.3e} FLOP ({china_row['share_pct']:.2f}%)\n"
        f"Rest of world total (Chart 2):         {row_row['total_compute_flop']:.3e} FLOP ({row_row['share_pct']:.2f}%)"
    ),
    tables={
        "Organization concentration summary": orgs,
    },
)

# ---------------------------------------------------------------- chart 2: country concentration
st.markdown(f"#### The United States accounts for {us_row['share_pct']:.0f}% of frontier AI training compute")

cntry_reset = countries.reset_index()
fig2 = go.Figure(go.Bar(
    x=cntry_reset["country"],
    y=cntry_reset["share_pct"],
    name="Country compute share (%)",
    marker=dict(color=[SERIES[0], SERIES[1], CONTEXT], line=dict(color=SURFACE, width=1.5)),
    text=[f"{v:.1f}%" for v in cntry_reset["share_pct"]],
    textposition="outside",
    textfont=dict(color=INK, size=13),
    hovertemplate="%{x}: %{y:.2f}% of notable training compute<extra></extra>",
))
fig2.update_yaxes(range=[0, 110], ticksuffix="%")
style(fig2, height=300, x_title="Country of organization headquarters",
      y_title="Share of training compute (%)", legend=False)
st.plotly_chart(fig2, config=PLOTLY_CONFIG, width="stretch")
st.caption(
    "Frontier model training compute share by country of organization headquarters, 2020–2026. "
    "United States leads with 90.6% (Blue), followed by China with 8.1% (Orange) and the rest of the world at 1.3% (Grey). "
    "These national totals match the sum of the corresponding blue, orange, and grey bars in Chart 1 above."
)

trace(
    sources=["EPOCH-MODELS"],
    files=[RAW_MODELS, PROC_CNTRY, "scripts/build_concentration.py"],
    steps=[
        "Grouped all post-2020 notable models by primary country of organization headquarters.",
        "Summed total training compute (FLOP) for the United States, China, and all other countries combined.",
        "Calculated country share: country FLOP / total post-2020 FLOP x 100.",
    ],
    worked_example=(
        f"United States compute: {us_row['total_compute_flop']:.3e} FLOP ({us_row['share_pct']:.2f}%)\n"
        f"China compute:         {china_row['total_compute_flop']:.3e} FLOP ({china_row['share_pct']:.2f}%)\n"
        f"Rest of world compute: {row_row['total_compute_flop']:.3e} FLOP ({row_row['share_pct']:.2f}%)"
    ),
    tables={
        "Country concentration summary": cntry_reset,
    },
)

# ---------------------------------------------------------------- takeaway for Daniel
with st.container(border=True):
    st.markdown(f"**What this means for {PERSONA['name']}**")
    st.markdown(
        f"For {PERSONA['name']} assessing data-centre development applications in Western Sydney, "
        f"this concentration reveals a crucial planning distinction:\n\n"
        f"- **Frontier training clusters** (the multi-gigawatt facilities driving exponential compute headlines) "
        f"are almost exclusively built by a small club of 4–5 US hyperscalers ({orgs.iloc[0]['organization']}, "
        f"{orgs.iloc[1]['organization']}, {orgs.iloc[2]['organization']}) in regions with massive, dedicated power infrastructure.\n"
        f"- **Local applications in Western Sydney** are predominantly enterprise colocation, cloud storage, "
        f"and inference hubs. These serve local users and have far flatter, more predictable power profiles.\n\n"
        f"{PERSONA['name']} should advise councillors to ask applicants explicitly what workloads their facility "
        f"will host. Standard enterprise cloud facilities do not exhibit the unconstrained exponential compute draw "
        f"seen in frontier AI training headlines."
    )
    st.markdown(
        "<span style='color:" + INK_2 + "'>Limits: covers notable published models tracked by Epoch AI; "
        "undisclosed private models and government programs are not in the dataset.</span>",
        unsafe_allow_html=True,
    )

with st.expander("Design notes: why these charts"):
    st.markdown(
        "- **Horizontal bar for organizations:** The visual task is ranking and comparing magnitude across 8 entities. "
        "Horizontal bars allow full organization names to read naturally from left to right without tilted text, "
        "and direct percentage labels mean readers do not need to hover.\n"
        "- **Color consistency across charts:** Colors consistently reflect geography across both charts: "
        "Blue (`#2a78d6`) for the United States and US-based organizations (OpenAI, xAI, Meta, Google DeepMind, Anthropic), "
        "Orange (`#eb6834`) for China and Chinese organizations (Alibaba), and Grey (`#b4b2a9`) for the rest of the world and industry. "
        "This avoids visual confusion and strictly follows the team's CVD-checked palette.\n"
        "- **Alternative rejected: a pie chart or treemap.** A pie chart asks readers to compare slice angles, "
        "which humans judge far less accurately than bar lengths, and thin slivers below 3% become illegible.\n"
        "- **Country column chart:** Compares the 3 discrete geographic segments on an honest 0–100% axis, "
        "highlighting the dramatic 90.6% US concentration."
    )
