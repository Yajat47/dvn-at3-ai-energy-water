"""Entry point. Registers every page so nobody needs to edit this file to add their own."""

import streamlit as st

st.set_page_config(page_title="AI's footprint: global or local?", layout="wide")

pages = {
    "The question": [
        st.Page("views/home.py", title="Home", icon=":material/home:", default=True),
    ],
    "The evidence": [
        st.Page("views/global_scale.py", title="1. Global scale", icon=":material/public:"),
        st.Page("views/where_it_lands.py", title="2. Where it lands", icon=":material/location_on:"),
        st.Page("views/compute_vs_efficiency.py", title="3. Compute vs efficiency", icon=":material/memory:"),
        st.Page("views/water.py", title="4. Water", icon=":material/water_drop:"),
    ],
    "Method": [
        st.Page("views/sources.py", title="Sources and method", icon=":material/fact_check:"),
    ],
}

st.navigation(pages).run()
