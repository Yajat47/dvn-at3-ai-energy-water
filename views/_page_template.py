"""Template for a page. Copy this into your page file, then replace every TODO.

Not registered in app.py, so it never shows in the app.
See views/global_scale.py for a complete example.
"""

import plotly.graph_objects as go
import streamlit as st

from utils import data
from utils.story import PERSONA, TEAM
from utils.theme import PLOTLY_CONFIG, SERIES, SURFACE, style
from utils.trace import trace

KEY = "where"  # TODO: your key in TEAM / STATUS (where, compute, water)
NEED = 1  # TODO: index of the persona question you answer (1, 2 or 3)

# TODO: produce this file with scripts/build_<page>.py from raw files in data/raw/
df = data.processed("TODO_your_processed_file")

st.title("TODO: page title")
st.subheader("TODO: one-line takeaway, written as a finding")
st.caption(f"Page owner: {TEAM[KEY]} · Answers {PERSONA['name']}'s question: \"{PERSONA['needs'][NEED]}\"")

st.markdown("TODO: two or three sentences. Compute every number from df, never type it in.")

st.markdown("#### TODO: chart title that states the finding")
fig = go.Figure()
fig.add_trace(go.Scatter(
    x=df["year"], y=df["value"], name="TODO", mode="lines+markers",
    line=dict(color=SERIES[0], width=2.5),
    marker=dict(size=8, color=SERIES[0], line=dict(color=SURFACE, width=2)),
))
style(fig, y_title="TODO unit")
st.plotly_chart(fig, config=PLOTLY_CONFIG, width="stretch")
st.caption("TODO: how to read it, and any gaps or caveats in the data.")

trace(
    sources=["TODO-SOURCE-ID"],  # must match a source_id in sources.csv
    files=["data/raw/TODO.csv", "data/processed/TODO.csv", "scripts/build_TODO.py"],
    steps=["TODO: step 1", "TODO: step 2"],
    worked_example="TODO: show the arithmetic for the headline number",
    tables={"Processed rows": df},
)

with st.container(border=True):
    st.markdown(f"**What this means for {PERSONA['name']}**")
    st.markdown("TODO")
