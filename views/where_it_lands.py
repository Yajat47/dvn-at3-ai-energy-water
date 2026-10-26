
from pathlib import Path
import pandas as pd
import plotly.graph_objects as go
import streamlit as st
from utils.theme import style, SERIES, CONTEXT, PLOTLY_CONFIG

ROOT = Path(__file__).resolve().parents[1]
FILE = 'data/samples/owid_data_centers_share_electricity_demand.csv'
FIELD = 'Share of total electricity demand coming from data centers'
st.title('2. Where it lands')
st.caption('Proposed contribution: national and regional comparison')
st.write('How does data-centre electricity demand compare across places?')
df = pd.read_csv(ROOT / FILE)
year = st.selectbox('Year', sorted(df.Year.unique()), index=len(df.Year.unique())-1)
entity = st.selectbox('Comparison', ['United States', 'China', 'Europe (IEA)', 'Asia Pacific (IEA)'])
selected = df[(df.Year == year) & df.Entity.isin([entity, 'World'])].copy()
selected = selected.set_index('Entity').loc[[entity, 'World']].reset_index()
values = selected[FIELD].tolist()
fig = go.Figure(go.Bar(x=values, y=selected.Entity, orientation='h',
    marker_color=[SERIES[0], CONTEXT], text=[f'{v:.2f}%' for v in values], textposition='outside'))
fig.update_xaxes(range=[0,6], ticksuffix='%')
fig.update_yaxes(autorange='reversed')
fig.update_layout(title=f'Data-centre electricity shares differ by place, {year}')
style(fig, x_title='Share of total electricity demand (%)', y_title='Country or region', legend=False)
st.plotly_chart(fig, config=PLOTLY_CONFIG)
ratio = values[0] / values[1]
st.write(f'In {year}, {entity} has {ratio:.2f} times the world share.')
st.caption('Each share uses its own geography’s electricity demand as denominator. Geographies overlap and must not be added. Fixed scale: 0–6%.')
with st.expander('Where does this number come from?'):
    st.write('Source: Our World in Data, using IEA and Ember. Group snapshot downloaded 20 October 2026.')
    st.code(FILE)
    st.dataframe(selected[['Entity','Year',FIELD]], hide_index=True)
    st.write('Filter by year and entity. Keep the source percentage as supplied. Round to two decimals only for display.')
    st.code(f'{values[0]} / {values[1]} = {ratio:.2f} times')
    lines = (ROOT / FILE).read_text().splitlines()
    prefixes = [f'{entity},', 'World,']
    st.code('\n'.join(line for line in lines if any(line.startswith(p) for p in prefixes) and f',{year},' in line))
    st.download_button('Download source CSV', (ROOT / FILE).read_bytes(), file_name=Path(FILE).name, mime='text/csv')
st.subheader('What Daniel can conclude')
st.write('National and regional shares differ from the global average. They justify investigating the local grid before drawing conclusions about a particular development.')
st.info('These figures cover all data centres. They cannot isolate AI electricity, water use, NSW, Ireland or Virginia. National shares do not establish local grid capacity.')

