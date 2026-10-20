# Research brief

Facts gathered on 20 October 2026 to help each page owner start. **Not on screen.** Before a number goes into the app, download the source file into `data/samples/`, rebuild it in a script, and add a `sources.csv` row.

"Checked" means read on the publisher's own page or file. "Secondary" means seen only in news coverage, so find the primary source first.

## Global scale (page 1, built)

| Fact | Number | Source | Status |
|---|---|---|---|
| Data-centre electricity, 2025 | 485 TWh, up 17% on 2024 | IEA, Key Questions on Energy and AI (2026) | Checked |
| AI-focused data centres, 2025 | grew 50% in the year; about 155 TWh | IEA 2026; TWh figure via Our World in Data | Checked |
| Projection, 2030 | 950 TWh, about 3% of world electricity; AI-focused use triples | IEA 2026 | Checked |
| Energy per AI task | "dropping by at least an order of magnitude annually in recent years" | IEA 2026 | Checked |
| Per-query energy | Gemini median text prompt about 0.24 Wh; agentic request with reasoning about 50 Wh | Google; IEA, via Our World in Data | Checked (OWID) |

Our World in Data still shows 945 TWh for 2030 (the IEA's 2025 figure). Use 950 TWh from the 2026 report.

## Where it lands (page 2)

| Fact | Number | Source | Status |
|---|---|---|---|
| Ireland, data-centre share of metered electricity | 5% (2015) to 23% (2025); 7,663 GWh in 2025, up 10%; households 28% | CSO, Data Centres Metered Electricity Consumption 2025, PxStat table MEC02 | Checked |
| United States share, 2025 | 4.9% | IEA via OWID (already in `data/samples/`) | Checked |
| Virginia | more than a quarter of the state's electricity | Our World in Data article | Checked (OWID) |
| NEM data centres, FY26 | about 165 sites, about 5 TWh, about 3% of NEM operational consumption | AEMO 2026 ESOO data-centre forecasting overview | Checked |
| NEM forecast, Step Change | about 15 TWh (7.8%) by FY30; about 34 TWh (13%) by FY36 | AEMO 2026 ESOO | Checked |
| NEM data-centre demand by state, FY26 | NSW 66%, Vic 30%, SA 2%, Qld 1%, Tas under 1% | AEMO 2026 ESOO | Checked |
| Pipeline | 225 projects, 67 GW; 36% of 2025 ESOO developing projects cancelled; grid-connection utilisation about 27% | AEMO 2026 ESOO | Checked |
| Concentration | Fewer than 10 regions hold nearly two-thirds of projected AI data-centre demand; Oregon, Ireland and Iowa face high relative pressure | Chen et al., Communications Sustainability (2026), via AZoRobotics | Secondary |

## Compute vs efficiency (page 3)

- Epoch AI publishes downloadable CSVs: Notable AI Models (training compute) and Machine Learning Hardware (performance per watt). https://epoch.ai/data
- IEA 2026: energy per AI task falling at least tenfold a year, but video generation, reasoning and agentic tasks can use hundreds or thousands of times more energy per query than simple text.
- Tension worth showing: Google's electricity use rose about 37% in 2025 despite efficiency gains (Google 2026 Environmental Report via press: secondary, check the PDF).

## Water (page 4)

| Fact | Number | Source | Status |
|---|---|---|---|
| Sydney data centres today | 88 data centres use about 3.5 GL a year, under 1% of supply | SmartCompany / Sydney Water reporting | Secondary |
| Sydney forecast | up to 250 ML a day by 2035 (Sydney Water submission to IPART); up to 25% of supply under high growth | press reporting | Secondary |
| Recycled water | Badu Yarragul plant at Kemps Creek (opened Sept 2026) treats 35 ML a day; Sydney Water says it could supply data centres | ABC, 6 Oct 2026 | Checked |
| Planning gap | Data-centre demand was not in the 2022 Greater Sydney Water Strategy (Prof. Stuart Khan) | ABC, 6 Oct 2026 | Checked |
| NSW pipeline | more than 60 operational data centres; 18 state-significant projects worth $61.22 billion | NSW Dept of Planning, via ABC | Checked |
| Google water, 2025 | figures differ between summaries (about 9.9 to 10.9 billion gallons) | Google 2026 Environmental Report | Check the PDF |

## Where the sources disagree (good material for the verdict)

- **Total size:** IEA 485 TWh vs Energy Institute / S&P Global about 790 TWh for 2025. Crypto mining (150 to 200 TWh) explains most of the gap.
- **AI-only:** Chen et al. estimate 118 TWh in 2024, rising to 239 to 295 TWh by 2030 (about 1% of world electricity), covering six large firms. That is well below the IEA's AI-focused path.
- **Forecast firmness:** AEMO's cancellation rate and the 27% utilisation figure argue for planning to a range, not a single number.

## Do not use

- "Data centres were 17% of global electricity demand growth in 2025" (Fortune). It looks like a mix-up with the IEA's "+17% growth" figure. The IEA's own numbers imply about 70 TWh added, roughly a tenth of global growth or less.
- "IEA projects 1,000 TWh by 2026" (tech-insider.org). Not traceable to the IEA.

## Links

- IEA Key Questions on Energy and AI: https://www.iea.org/reports/key-questions-on-energy-and-ai/executive-summary
- Our World in Data article: https://ourworldindata.org/how-much-energy-do-data-centers-and-artificial-intelligence-use
- CSO Ireland 2025 release: https://www.cso.ie/en/releasesandpublications/ep/p-dcmec/datacentresmeteredelectricityconsumption2025/
- AEMO 2026 ESOO data-centre overview: https://www.aemo.com.au/-/media/files/electricity/nem/planning_and_forecasting/nem_esoo/2026/2026-esoo-data-centre-forecasting-overview.pdf
- Chen et al. 2026: https://www.nature.com/articles/s44458-026-00152-5
- ABC, 6 Oct 2026: https://www.abc.net.au/news/2026-10-06/nsw-sydney-recycled-water-earmarked-for-ai-data-centres/107214474
- SmartCompany: https://www.smartcompany.com.au/technology/data-centres-to-overtake-breweries-sydneys-biggest-water-users/
- Google 2026 Environmental Report: https://sustainability.google/files/google-2026-environmental-report.pdf
- WRI Aqueduct: https://www.wri.org/aqueduct
