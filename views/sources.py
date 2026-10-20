"""Sources and method. Owner: Yajat. Every source used anywhere in the app must be a row in sources.csv."""

import streamlit as st

from utils import data

st.title("Sources and method")
st.markdown(
    "Every number in this app can be traced to a file in the repository. Data moves one way:\n\n"
    "1. **`data/raw/`** holds downloads exactly as published. Nobody edits these.\n"
    "2. **`data/raw/manual/`** holds numbers copied from report text, with the original sentence stored "
    "word for word next to each number.\n"
    "3. **`scripts/`** turns raw files into processed files. Every step is in code.\n"
    "4. **`data/processed/`** is what the pages read.\n"
    "5. Each chart has a **Where does this number come from?** box listing its sources, files and steps."
)

st.markdown("### Source registry")
reg = data.sources()
st.dataframe(
    reg,
    hide_index=True,
    width="stretch",
    column_config={"url": st.column_config.LinkColumn("url", display_text="open")},
)

st.markdown("### Processed files")
for f in sorted(data.PROCESSED.glob("*.csv")):
    c1, c2 = st.columns([4, 1])
    c1.markdown(f"`data/processed/{f.name}`")
    c2.download_button("Download", f.read_bytes(), file_name=f.name, mime="text/csv", key=f.name)

st.markdown("### Rebuild everything")
st.code("python scripts/fetch_raw.py      # re-download raw files\npython scripts/build_global.py   # page 1 tables",
        language="bash")
