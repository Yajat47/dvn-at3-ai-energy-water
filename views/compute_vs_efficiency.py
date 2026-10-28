"""3. Compute vs efficiency: is chip efficiency keeping pace with the growth in AI training compute?

Owner: Niki. Data built by scripts/build_compute.py.
"""

import math

import plotly.graph_objects as go
import streamlit as st

from utils import data
from utils.story import PERSONA, TEAM
from utils.theme import INK, INK_2, PLOTLY_CONFIG, SERIES, SURFACE, style
from utils.trace import trace

KEY = "compute"
NEED = 2  # "Will efficiency gains cancel out the growth?"

RAW_MODELS = "data/samples/epoch_notable_ai_models.csv"
RAW_HW = "data/samples/epoch_ml_hardware.csv"
PROC = "data/processed/compute_vs_efficiency.csv"
PROC_SUMMARY = "data/processed/compute_growth_summary.csv"

COMPUTE = "Training compute of the largest model"
EFFICIENCY = "Efficiency of the best chip (FP32)"
SHORT = {COMPUTE: "Training compute (largest model)", EFFICIENCY: "Chip efficiency (best FP32 chip)"}
COLOUR = {COMPUTE: SERIES[0], EFFICIENCY: SERIES[1]}


def times(x: float) -> str:
    """A growth multiple written for people: 1, 28, 4.6 thousand, 345 million."""
    if x >= 1e9:
        return f"{x / 1e9:.3g} billion"
    if x >= 1e6:
        return f"{x / 1e6:.3g} million"
    if x >= 1e4:
        return f"{x / 1e3:.3g} thousand"
    return f"{x:,.3g}" if x < 100 else f"{x:,.0f}"


def short_times(x: float) -> str:
    """Compact label for chart points: x1, x28, x4.6k, x345M."""
    if x >= 1e9:
        return f"x{x / 1e9:.3g}B"
    if x >= 1e6:
        return f"x{x / 1e6:.3g}M"
    if x >= 1e3:
        return f"x{x / 1e3:.3g}k"
    return f"x{x:.3g}"


def growth_stats(part, start: int, end: int) -> dict:
    """Total multiple, average yearly growth and doubling time between two years of one series."""
    v = part.set_index("year")["value"]
    multiple = v.loc[end] / v.loc[start]
    per_year = multiple ** (1 / (end - start))
    doubling = 12 * math.log(2) / math.log(per_year) if per_year > 1 else math.inf
    return {"multiple": multiple, "per_year": per_year, "doubling_months": doubling}


# ---------------------------------------------------------------- data
df = data.processed("compute_vs_efficiency")
summary = data.processed("compute_growth_summary").set_index("series")
first_year, last_year = int(df["year"].min()), int(df["year"].max())
series = {name: df[df["series"] == name].sort_values("year") for name in (COMPUTE, EFFICIENCY)}

# The raw rows behind the first and last records, for the worked example in the trace box.
FP32 = "FP32 (single precision) performance (FLOP/s)"
models_raw = data.sample("epoch_notable_ai_models.csv").set_index("Model", drop=False)
hw_raw = data.sample("epoch_ml_hardware.csv").set_index("Hardware name", drop=False)


def record_row(raw, name: str, year: int):
    holder = series[name].set_index("year").loc[year, "record_holder"]
    return raw.loc[holder]


# Headline numbers for the full period come from the summary file, so the text matches the trace box.
full_c, full_e = summary.loc[COMPUTE], summary.loc[EFFICIENCY]
m_start, m_end = record_row(models_raw, COMPUTE, first_year), record_row(models_raw, COMPUTE, last_year)
h_start, h_end = record_row(hw_raw, EFFICIENCY, first_year), record_row(hw_raw, EFFICIENCY, last_year)

st.title("3. Compute vs efficiency")
st.subheader("Chip efficiency is improving, but nowhere near as fast as the compute used to train AI")
st.caption(f"Page owner: {TEAM[KEY]} · Answers {PERSONA['name']}'s question: \"{PERSONA['needs'][NEED]}\"")

st.markdown(
    f"From {first_year} to {last_year}, the training compute of the largest AI model grew about "
    f"**{times(full_c['total_multiple'])} times**, doubling every **{full_c['doubling_time_months']:.1f} months**. "
    f"Over the same years the most energy-efficient chip improved about **{times(full_e['total_multiple'])} times**, "
    f"doubling every **{full_e['doubling_time_months']:.1f} months**. Both lines show records: the biggest model and "
    "the most efficient chip released up to each year, from Epoch AI's public datasets."
)

# ---------------------------------------------------------------- control
start = st.select_slider(
    "Start the comparison in",
    options=list(range(first_year, last_year - 4)),  # at least five years of change
    value=first_year,
    key=f"{KEY}_start",
    help="Both lines are re-indexed so the chosen year = 1. Later starts show whether the gap is recent.",
)
stats = {name: growth_stats(part, start, last_year) for name, part in series.items()}
gap = stats[COMPUTE]["multiple"] / stats[EFFICIENCY]["multiple"]

k1, k2, k3 = st.columns(3)
k1.metric(f"Training compute, {start} to {last_year}", f"x{times(stats[COMPUTE]['multiple'])}",
          f"x{stats[COMPUTE]['per_year']:.2f} a year", delta_color="off", border=True)
k2.metric(f"Chip efficiency, {start} to {last_year}", f"x{times(stats[EFFICIENCY]['multiple'])}",
          f"x{stats[EFFICIENCY]['per_year']:.2f} a year", delta_color="off", border=True)
k3.metric("Compute growth ÷ efficiency growth", f"{times(gap)}",
          "How many times further compute has grown", delta_color="off", border=True,
          help="The compute multiple divided by the efficiency multiple over the chosen years. "
               "It compares two indexes; it is not an energy figure.")

# ---------------------------------------------------------------- chart 1: indexed lines, log axis
st.markdown(f"#### Since {start}, compute has grown {times(gap)} times further than chip efficiency")
fig = go.Figure()
for name, part in series.items():
    part = part[part["year"] >= start]
    base = part["value"].iloc[0]
    index = part["value"] / base
    # Label the start, every year a new record is set, and the last year, so labels never pile up.
    new_record = part["record_year"].ne(part["record_year"].shift()) | (part["year"] == last_year)
    labels = [short_times(v) if show else "" for v, show in zip(index, new_record)]
    fig.add_trace(go.Scatter(
        x=part["year"], y=index, name=SHORT[name], mode="lines+markers+text",
        text=labels, textposition="top center" if name == COMPUTE else "bottom center",
        textfont=dict(color=INK, size=12),
        line=dict(color=COLOUR[name], width=2.5),
        marker=dict(size=7, color=COLOUR[name], line=dict(color=SURFACE, width=2)),
        customdata=part[["record_holder", "record_organization", "record_year"]],
        hovertemplate="%{y:,.3g} times the " + str(start) + " level<br>Record: %{customdata[0]} "
                      "(%{customdata[1]}, %{customdata[2]})<extra>" + SHORT[name] + "</extra>",
    ))
style(fig, height=460, x_title="Year", y_title=f"Index, {start} = 1 (log scale)",
      legend_title=f"Record to date (index, {start} = 1)")
fig.update_yaxes(type="log", rangemode="normal", dtick=1, exponentformat="power")
st.plotly_chart(fig, config=PLOTLY_CONFIG, width="stretch")
st.caption(
    f"Index, {start} = 1, on a log scale: each gridline is ten times the one below. Years {start} to {last_year}. "
    "Training compute is total floating-point operations (FLOP) used to train the largest model released so far. "
    "Chip efficiency is FP32 FLOP per second divided by the chip's rated power (TDP, watts), best chip released so "
    "far. FP32 is the one precision Epoch AI reports across the whole period; modern AI chips are faster at lower "
    "precisions, so this understates recent chips, and the line stays flat after 2022 because no later chip in the "
    "file beats that FP32 record."
)

trace(
    sources=["EPOCH-MODELS", "EPOCH-HARDWARE"],
    files=[RAW_MODELS, RAW_HW, PROC, PROC_SUMMARY, "scripts/build_compute.py"],
    steps=[
        "Models: kept rows with a publication date and a positive training compute (FLOP).",
        "Chips: kept rows with a release date, FP32 performance and TDP; efficiency = FP32 FLOP/s / TDP watts.",
        "For each year, kept the record released up to and including that year (largest model, most efficient chip), so neither line can fall.",
        f"Indexed each line to its {first_year} value = 1 in the processed file; this page re-indexes to the start year you choose.",
        "Average growth per year = (last / first) ^ (1 / years); doubling time = 12 x ln 2 / ln(growth per year) months.",
    ],
    worked_example=(
        f"Largest model, {last_year}: {m_end['Model']} ({m_end['Organization']})   "
        f"{m_end['Training compute (FLOP)']:.4g} FLOP   (raw models file)\n"
        f"Largest model, {first_year}: {m_start['Model']} ({m_start['Organization']}, {m_start['Publication date'][:4]})   "
        f"{m_start['Training compute (FLOP)']:.4g} FLOP\n"
        f"Compute multiple      {m_end['Training compute (FLOP)']:.4g} / {m_start['Training compute (FLOP)']:.4g} "
        f"= {full_c['total_multiple']:.3g}\n"
        f"Best chip, {last_year}: {h_end['Hardware name']}   {h_end[FP32]:.4g} FLOP/s / {h_end['TDP (W)']:.0f} W "
        f"= {h_end[FP32] / h_end['TDP (W)']:.3g} FLOP/s per W\n"
        f"Best chip, {first_year}: {h_start['Hardware name']}   {h_start[FP32]:.4g} FLOP/s / {h_start['TDP (W)']:.0f} W "
        f"= {h_start[FP32] / h_start['TDP (W)']:.3g} FLOP/s per W\n"
        f"Efficiency multiple   {full_e['end_value']:.3g} / {full_e['start_value']:.3g} = {full_e['total_multiple']:.3g}\n"
        f"Compute growth a year {full_c['total_multiple']:.3g} ^ (1/{last_year - first_year}) = {full_c['growth_per_year']:.2f}"
    ),
    exact_rows=[
        (f"{m_end['Model']} training compute", RAW_MODELS, f"{m_end['Model']},"),
        (f"{m_start['Model']} training compute", RAW_MODELS, f"{m_start['Model']},"),
        (f"{h_end['Hardware name']} FP32 and TDP", RAW_HW, f"{h_end['Hardware name']},"),
        (f"{h_start['Hardware name']} FP32 and TDP", RAW_HW, f"{h_start['Hardware name']},"),
    ],
    tables={"Processed rows used in this chart": df, "Growth summary": summary.reset_index()},
)

# ---------------------------------------------------------------- chart 2: doubling time
st.markdown(
    f"#### Compute doubles every {stats[COMPUTE]['doubling_months']:.1f} months; "
    f"chip efficiency every {stats[EFFICIENCY]['doubling_months']:.1f}"
)
names = [EFFICIENCY, COMPUTE]
months = [stats[n]["doubling_months"] for n in names]
bar = go.Figure(go.Bar(
    y=[SHORT[n] for n in names], x=months, orientation="h", name=f"Doubling time, {start} to {last_year}",
    marker=dict(color=[COLOUR[n] for n in names], line=dict(color=SURFACE, width=2)),
    text=[f"{m:.1f} months" if math.isfinite(m) else "no gain" for m in months], textposition="outside",
    textfont=dict(color=INK, size=13),
    hovertemplate="%{x:.1f} months<extra></extra>",
))
style(bar, height=240, x_title="Months to double (shorter = faster growth)", y_title="Measure",
      legend_title=f"Average doubling time, {start} to {last_year} (months)", legend=False)
bar.update_xaxes(range=[0, max(m for m in months if math.isfinite(m)) * 1.25])
st.plotly_chart(bar, config=PLOTLY_CONFIG, width="stretch")
st.caption(
    f"Months, average over {start} to {last_year}, from the same records as the chart above: "
    "12 x ln 2 / ln(average yearly growth). A shorter bar means faster growth."
)

with st.container(border=True):
    st.markdown(f"**What this means for {PERSONA['name']}**")
    st.markdown(
        f"Better chips do cut the energy needed per calculation, but over {start} to {last_year} the calculations "
        f"behind the largest models grew about {times(gap)} times further. On this evidence {PERSONA['name']} "
        "should not assume efficiency will level off data-centre demand by itself. This page compares records, "
        "not total electricity: how much energy that compute actually draws depends on how many chips run, how "
        "busy they are, and cooling, which page 1's IEA figures capture."
    )
    st.markdown(
        "<span style='color:" + INK_2 + "'>Limits: frontier records only, not the average model or chip; "
        "efficiency is FP32 per rated watt, not measured power.</span>",
        unsafe_allow_html=True,
    )

with st.expander("Design notes: why this chart"):
    st.markdown(
        "- **Visual task:** compare the growth rates of two series measured in different units (FLOP and FLOP/s per W).\n"
        "- **Form chosen:** both lines indexed to the start year = 1 on one log axis, so the gap between the "
        "lines is the gap in growth.\n"
        "- **Alternative rejected: a dual y-axis chart** with FLOP on the left and FLOP/s per W on the right. "
        "With two scales the lines can be made to cross or run together just by moving either axis, so the "
        "picture would show our axis choice, not the data. Indexing to a common base removes the unit problem "
        "honestly (the team's chart rules also rule out dual axes).\n"
        "- **Also rejected: a linear axis.** Compute grows by about eight orders of magnitude, so on a linear "
        "axis the efficiency line sits flat on zero and every year before 2023 is invisible.\n"
        "- **Labels only on new records** and the last year, so every change can be read without hovering "
        "and the labels never overlap."
    )
