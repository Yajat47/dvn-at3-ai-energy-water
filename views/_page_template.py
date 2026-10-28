"""Template for a page. Copy this into your page file, then replace every TODO.

Not registered in app.py, so it never shows in the app. views/global_scale.py is a complete example.
Before your PR: python scripts/build_all.py, then python scripts/check_package.py (no new FAILs).
"""

import plotly.graph_objects as go
import streamlit as st

from utils import data
from utils.story import PERSONA, TEAM
from utils.theme import INK, PLOTLY_CONFIG, SERIES, SURFACE, style
from utils.trace import trace

KEY = "where"  # TODO: your key in TEAM (where, compute, water)
NEED = 1  # TODO: index of the persona question you answer (1, 2 or 3)

# TODO: produce this file with scripts/build_<page>.py from your files in data/samples/,
# and describe both in data/data_dictionary.yml.
df = data.processed("TODO_your_processed_file")

st.title("TODO: page title")
st.subheader("TODO: one-line takeaway, written as a finding")
st.caption(f"Page owner: {TEAM[KEY]} · Answers {PERSONA['name']}'s question: \"{PERSONA['needs'][NEED]}\"")

st.markdown("TODO: two or three sentences. Compute every number from df, never type it in.")

# ---- chart: title states the finding; control above; empty state; labels on every value
st.markdown("#### TODO: chart title that states the finding")
options = sorted(df["TODO_category_column"].unique())
chosen = st.multiselect("TODO: label", options, default=options, key=f"{KEY}_filter")
if not chosen:
    st.info("Nothing selected. Choose at least one TODO above.", icon=":material/filter_alt_off:")
else:
    fig = go.Figure()
    for i, name in enumerate(chosen[:3]):  # three colours max; fold the rest into "Other" or facet
        part = df[df["TODO_category_column"] == name]
        fig.add_trace(go.Scatter(
            x=part["year"], y=part["value"], name=name, mode="lines+markers+text",
            text=[f"{v:.1f}" for v in part["value"]], textposition="top center", textfont=dict(color=INK),
            line=dict(color=SERIES[i], width=2.5),
            marker=dict(size=8, color=SERIES[i], line=dict(color=SURFACE, width=2)),
        ))
    style(fig, x_title="Year", y_title="TODO measure (unit)", legend_title="TODO series (unit)")
    st.plotly_chart(fig, config=PLOTLY_CONFIG, width="stretch")
    st.caption("TODO: what the chart shows, the unit, the baseline, the years covered, and any gaps.")

trace(
    sources=["TODO-SOURCE-ID"],  # must match a source id in data/data_dictionary.yml
    files=["data/samples/TODO.csv", "data/processed/TODO.csv", "scripts/build_TODO.py"],
    steps=["TODO: step 1", "TODO: step 2"],
    worked_example="TODO: show the arithmetic for the headline number",
    tables={"Processed rows": df},
)

with st.container(border=True):
    st.markdown(f"**What this means for {PERSONA['name']}**")
    st.markdown("TODO: one or two sentences that stay within what the data shows.")
