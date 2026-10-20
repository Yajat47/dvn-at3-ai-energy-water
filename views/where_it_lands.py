"""2. Where it lands. Owner: Member A. Replace this placeholder with your page."""

from utils.stub import coming_soon

coming_soon(
    key="where",
    title="2. Where it lands",
    need=1,
    brief=(
        "Show how large the data-centre share is in the grids it actually connects to, compared with the "
        "global share on page 1. Cover Ireland, US hubs such as Virginia, and Australia's National Electricity "
        "Market, with NSW highlighted for the persona."
    ),
    sources=[
        ("CSO Ireland: Data Centres Metered Electricity Consumption 2025 (PxStat table MEC02)",
         "https://www.cso.ie/en/releasesandpublications/ep/p-dcmec/datacentresmeteredelectricityconsumption2025/"),
        ("AEMO 2026 ESOO: data centre forecasting overview (PDF)",
         "https://www.aemo.com.au/-/media/files/electricity/nem/planning_and_forecasting/nem_esoo/2026/2026-esoo-data-centre-forecasting-overview.pdf"),
        ("Our World in Data: data-centre share of electricity by region (already in data/samples/)",
         "https://ourworldindata.org/grapher/data-centers-share-electricity-demand"),
    ],
)
