# Data dictionary

Generated from `data/data_dictionary.yml` by `scripts/build_all.py`. Edit the YAML, not this file.

## Sources

| ID | Title | Publisher | URL | Licence | Retrieved |
|---|---|---|---|---|---|
| `IEA-2026-KQ` | Key Questions on Energy and AI (executive summary) | International Energy Agency | https://www.iea.org/reports/key-questions-on-energy-and-ai/executive-summary | IEA terms of use (figures quoted with attribution) | 2026-10-20 |
| `OWID-DC-SHARE` | Share of total electricity demand used by data centers | Our World in Data, based on IEA (2025, 2026) and Ember (2026) | https://ourworldindata.org/grapher/data-centers-share-electricity-demand | CC BY 4.0 (Our World in Data processing); underlying IEA data under IEA terms | 2026-10-20 |
| `OWID-EMBER-DEMAND` | Electricity demand | Our World in Data, based on Ember (2026) | https://ourworldindata.org/grapher/electricity-demand | CC BY 4.0 | 2026-10-20 |
| `GOOGLE-2026-ENV` | Environmental Report 2026 | Google | https://sustainability.google/files/google-2026-environmental-report.pdf | Company report (figures quoted with attribution) | 2026-10-26 |
| `EPOCH-MODELS` | Notable AI Models | Epoch AI | https://epoch.ai/data/notable-ai-models | CC BY 4.0 | 2026-10-21 |
| `EPOCH-HARDWARE` | Machine Learning Hardware | Epoch AI | https://epoch.ai/data/machine-learning-hardware | CC BY 4.0 | 2026-10-21 |

## Source samples

### `data/samples/owid_data_centers_share_electricity_demand.csv`

IEA data-centre electricity use as a share of each region's electricity demand.

- **Dataset ID:** `owid_dc_share` (owner: Yajat)
- **Source:** Our World in Data, based on IEA (2025, 2026) and Ember (2026), *Share of total electricity demand used by data centers*
- **URL:** https://ourworldindata.org/grapher/data-centers-share-electricity-demand
- **Licence:** CC BY 4.0 (Our World in Data processing); underlying IEA data under IEA terms
- **Primary key:** `Entity`, `Year`
- **Time coverage:** 2020 and 2023-2025 (the IEA publishes no 2021-2022 estimates)
- **Latest observation:** 2025
- **Source metadata:** `data/samples/owid_data_centers_share_electricity_demand.metadata.json`
- **Transform:** Downloaded unchanged from the OWID grapher CSV export by scripts/fetch_sources.py.

| Column | Type | Unit | Description |
|---|---|---|---|
| `Entity` | string | none | Country or IEA region name |
| `Code` | string | none | ISO 3166-1 alpha-3 code; empty for regions, OWID_WRL for World |
| `Year` | integer | year | Calendar year |
| `Share of total electricity demand coming from data centers` | number | % | Data-centre electricity use divided by total electricity demand, x 100 |

### `data/samples/owid_ember_electricity_demand.csv`

Total electricity demand (generation adjusted for imports and exports) by country and region.

- **Dataset ID:** `owid_ember_demand` (owner: Yajat)
- **Source:** Our World in Data, based on Ember (2026), *Electricity demand*
- **URL:** https://ourworldindata.org/grapher/electricity-demand
- **Licence:** CC BY 4.0
- **Primary key:** `Entity`, `Year`
- **Time coverage:** 1990-2025 (varies by entity)
- **Latest observation:** 2025
- **Source metadata:** `data/samples/owid_ember_electricity_demand.metadata.json`
- **Transform:** Downloaded unchanged from the OWID grapher CSV export by scripts/fetch_sources.py.

| Column | Type | Unit | Description |
|---|---|---|---|
| `Entity` | string | none | Country or region name |
| `Code` | string | none | ISO 3166-1 alpha-3 code; empty for regions |
| `Year` | integer | year | Calendar year |
| `Electricity demand` | number | TWh | Total electricity demand in terawatt-hours |

### `data/samples/manual/iea_2026_key_questions.csv`

Headline numbers copied from the IEA report text, each with the sentence it came from.

- **Dataset ID:** `iea_2026_key_numbers` (owner: Yajat)
- **Source:** International Energy Agency, *Key Questions on Energy and AI (executive summary)*
- **URL:** https://www.iea.org/reports/key-questions-on-energy-and-ai/executive-summary
- **Licence:** IEA terms of use (figures quoted with attribution)
- **Primary key:** `metric`, `year`
- **Time coverage:** 2025 (actual) and 2030 (projection)
- **Latest observation:** 2025
- **Transform:** Typed in by hand from the report web page; the quote column holds each sentence word for word.

| Column | Type | Unit | Description |
|---|---|---|---|
| `metric` | string | none | What the number measures |
| `year` | integer | year | Year the number refers to |
| `value` | number | see unit column | The number as printed in the report |
| `unit` | string | none | Unit of value (TWh or %) |
| `kind` | string | none | actual or projection |
| `source_id` | string | none | Source id in this dictionary |
| `quote` | string | none | The report sentence, word for word |

### `data/samples/manual/google_2026_water.csv`

Water figures copied from the Google 2026 Environmental Report (water stewardship section), each with the phrase it came from.

- **Dataset ID:** `google_2026_water_numbers` (owner: Akil)
- **Source:** Google, *Environmental Report 2026*
- **URL:** https://sustainability.google/files/google-2026-environmental-report.pdf
- **Licence:** Company report (figures quoted with attribution)
- **Primary key:** `metric`, `year`
- **Time coverage:** 2025 (the report gives one-year figures and a 2024 to 2025 growth rate)
- **Latest observation:** 2025
- **Transform:** Typed in by hand from the report PDF; the quote column holds the report's own words for each number.

| Column | Type | Unit | Description |
|---|---|---|---|
| `metric` | string | none | What the number measures |
| `year` | integer | year | Year the number refers to |
| `value` | number | see unit column | The number as printed in the report |
| `unit` | string | none | Unit of value (billion_gallons or %) |
| `kind` | string | none | actual: reported by the company |
| `source_id` | string | none | Source id in this dictionary |
| `quote` | string | none | Words from the report, word for word |

### `data/samples/epoch_notable_ai_models.csv`

Epoch AI's list of notable AI models with training compute, parameters and publication date.

- **Dataset ID:** `epoch_notable_ai_models` (owner: Niki)
- **Source:** Epoch AI, *Notable AI Models*
- **URL:** https://epoch.ai/data/notable-ai-models
- **Licence:** CC BY 4.0
- **Primary key:** `Model`
- **Time coverage:** 1950-2026 (models published up to the retrieval date)
- **Latest observation:** 2026-09-30
- **Transform:** Downloaded unchanged from https://epoch.ai/data/notable_ai_models.csv by scripts/fetch_sources.py.

| Column | Type | Unit | Description |
|---|---|---|---|
| `Model` | string | none | Model name as published by Epoch AI |
| `Organization` | string | none | Developer organisation(s) |
| `Publication date` | date | date | Date the model was published (YYYY-MM-DD) |
| `Domain` | string | none | Epoch AI field, kept exactly as published; not used by this app |
| `Task` | string | none | Epoch AI field, kept exactly as published; not used by this app |
| `Parameters` | number | none | Epoch AI field, kept exactly as published; not used by this app |
| `Parameters notes` | string | none | Epoch AI field, kept exactly as published; not used by this app |
| `Training compute (FLOP)` | number | FLOP | Total floating-point operations used to train the model; used by build_compute.py |
| `Training compute notes` | string | none | Epoch AI field, kept exactly as published; not used by this app |
| `Training dataset` | string | none | Epoch AI field, kept exactly as published; not used by this app |
| `Training dataset size (total)` | string | none | Epoch AI field, kept exactly as published; not used by this app |
| `Dataset size notes` | string | none | Epoch AI field, kept exactly as published; not used by this app |
| `Confidence` | string | none | Epoch AI field, kept exactly as published; not used by this app |
| `Link` | string | none | Epoch AI field, kept exactly as published; not used by this app |
| `Reference` | string | none | Epoch AI field, kept exactly as published; not used by this app |
| `Citations` | number | none | Epoch AI field, kept exactly as published; not used by this app |
| `Authors` | string | none | Epoch AI field, kept exactly as published; not used by this app |
| `Abstract` | string | none | Epoch AI field, kept exactly as published; not used by this app |
| `Organization categorization` | string | none | Epoch AI field, kept exactly as published; not used by this app |
| `Country (of organization)` | string | none | Epoch AI field, kept exactly as published; not used by this app |
| `Notability criteria` | string | none | Epoch AI field, kept exactly as published; not used by this app |
| `Notability criteria notes` | string | none | Epoch AI field, kept exactly as published; not used by this app |
| `Epochs` | number | none | Epoch AI field, kept exactly as published; not used by this app |
| `Training time (hours)` | number | hours | Epoch AI field, kept exactly as published; not used by this app |
| `Training time notes` | string | none | Epoch AI field, kept exactly as published; not used by this app |
| `Training hardware` | string | none | Epoch AI field, kept exactly as published; not used by this app |
| `Hardware quantity` | number | none | Epoch AI field, kept exactly as published; not used by this app |
| `Hardware utilization (MFU)` | number | none | Epoch AI field, kept exactly as published; not used by this app |
| `Training compute cost (2023 USD)` | number | 2023 USD | Epoch AI field, kept exactly as published; not used by this app |
| `Compute cost notes` | string | none | Epoch AI field, kept exactly as published; not used by this app |
| `Training power draw (W)` | number | W | Epoch AI field, kept exactly as published; not used by this app |
| `Base model` | string | none | Epoch AI field, kept exactly as published; not used by this app |
| `Finetune compute (FLOP)` | number | FLOP | Epoch AI field, kept exactly as published; not used by this app |
| `Finetune compute notes` | string | none | Epoch AI field, kept exactly as published; not used by this app |
| `Batch size` | number | none | Epoch AI field, kept exactly as published; not used by this app |
| `Batch size notes` | string | none | Epoch AI field, kept exactly as published; not used by this app |
| `Model accessibility` | string | none | Epoch AI field, kept exactly as published; not used by this app |
| `Training code accessibility` | string | none | Epoch AI field, kept exactly as published; not used by this app |
| `Inference code accessibility` | string | none | Epoch AI field, kept exactly as published; not used by this app |
| `Accessibility notes` | string | none | Epoch AI field, kept exactly as published; not used by this app |
| `Numerical format` | string | none | Epoch AI field, kept exactly as published; not used by this app |
| `Frontier model` | string | none | Epoch AI field, kept exactly as published; not used by this app |
| `Hardware acquisition cost` | number | none | Epoch AI field, kept exactly as published; not used by this app |
| `Hardware utilization (HFU)` | number | none | Epoch AI field, kept exactly as published; not used by this app |
| `Training compute cost (cloud)` | number | none | Epoch AI field, kept exactly as published; not used by this app |
| `Training compute cost (upfront)` | number | none | Epoch AI field, kept exactly as published; not used by this app |
| `Open model weights?` | string | none | Epoch AI field, kept exactly as published; not used by this app |

### `data/samples/epoch_ml_hardware.csv`

Epoch AI's list of machine-learning chips with performance at each precision, power (TDP) and release date.

- **Dataset ID:** `epoch_ml_hardware` (owner: Niki)
- **Source:** Epoch AI, *Machine Learning Hardware*
- **URL:** https://epoch.ai/data/machine-learning-hardware
- **Licence:** CC BY 4.0
- **Primary key:** `Hardware name`
- **Time coverage:** 2008-2026 (chips released up to the retrieval date)
- **Latest observation:** 2026-09-30
- **Transform:** Downloaded unchanged from https://epoch.ai/data/ml_hardware.csv by scripts/fetch_sources.py.

| Column | Type | Unit | Description |
|---|---|---|---|
| `Hardware name` | string | none | Chip name as published by Epoch AI |
| `Manufacturer` | string | none | Chip manufacturer |
| `Type` | string | none | Epoch AI field, kept exactly as published; not used by this app |
| `Notes` | string | none | Epoch AI field, kept exactly as published; not used by this app |
| `Release date` | date | date | Date the chip was released (YYYY-MM-DD) |
| `Release price (USD)` | number | USD | Epoch AI field, kept exactly as published; not used by this app |
| `Tensor-FP16/BF16 performance (FLOP/s)` | number | FLOP/s | Epoch AI field, kept exactly as published; not used by this app |
| `FP8 performance (FLOP/s)` | number | FLOP/s | Epoch AI field, kept exactly as published; not used by this app |
| `FP4 performance (FLOP/s)` | number | FLOP/s | Epoch AI field, kept exactly as published; not used by this app |
| `Memory (bytes)` | number | bytes | Epoch AI field, kept exactly as published; not used by this app |
| `Memory bandwidth (byte/s)` | number | byte/s | Epoch AI field, kept exactly as published; not used by this app |
| `Intranode bandwidth (byte/s)` | number | byte/s | Epoch AI field, kept exactly as published; not used by this app |
| `Internode bandwidth (bit/s)` | number | bit/s | Epoch AI field, kept exactly as published; not used by this app |
| `TDP (W)` | number | W | Thermal design power, the rated power draw in watts; used by build_compute.py |
| `FP64 (double precision) performance (FLOP/s)` | number | FLOP/s | Epoch AI field, kept exactly as published; not used by this app |
| `FP32 (single precision) performance (FLOP/s)` | number | FLOP/s | Peak FP32 operations per second; used by build_compute.py |
| `TF32 (TensorFloat-32) performance (FLOP/s)` | number | FLOP/s | Epoch AI field, kept exactly as published; not used by this app |
| `FP16 (half precision) performance (FLOP/s)` | number | FLOP/s | Epoch AI field, kept exactly as published; not used by this app |
| `INT16 performance (OP/s)` | number | OP/s | Epoch AI field, kept exactly as published; not used by this app |
| `INT8 performance (OP/s)` | number | OP/s | Epoch AI field, kept exactly as published; not used by this app |
| `INT4 performance (OP/s)` | number | OP/s | Epoch AI field, kept exactly as published; not used by this app |
| `Foundry` | string | none | Epoch AI field, kept exactly as published; not used by this app |
| `Die Size (mm^2)` | number | mm^2 | Epoch AI field, kept exactly as published; not used by this app |
| `Base clock (MHz)` | number | MHz | Epoch AI field, kept exactly as published; not used by this app |
| `Boost clock (MHz)` | number | MHz | Epoch AI field, kept exactly as published; not used by this app |
| `Memory clock (MHz)` | number | MHz | Epoch AI field, kept exactly as published; not used by this app |
| `Memory bus (bit)` | number | bit | Epoch AI field, kept exactly as published; not used by this app |
| `Tensor cores` | number | none | Epoch AI field, kept exactly as published; not used by this app |
| `Process size (nm)` | number | nm | Epoch AI field, kept exactly as published; not used by this app |
| `Transistors (millions)` | number | millions | Epoch AI field, kept exactly as published; not used by this app |
| `Link to datasheet` | string | none | Epoch AI field, kept exactly as published; not used by this app |
| `Source for the price` | string | none | Epoch AI field, kept exactly as published; not used by this app |
| `ML models` | string | none | Epoch AI field, kept exactly as published; not used by this app |
| `Last modified` | string | none | Epoch AI field, kept exactly as published; not used by this app |
| `Max performance` | number | none | Epoch AI field, kept exactly as published; not used by this app |
| `Energy efficiency` | number | none | Epoch AI field, kept exactly as published; not used by this app |
| `Total processing performance (bit-OP/s)` | number | bit-OP/s | Epoch AI field, kept exactly as published; not used by this app |
| `Price-performance` | number | none | Epoch AI field, kept exactly as published; not used by this app |
| `ML OP/s` | number | none | Epoch AI field, kept exactly as published; not used by this app |
| `Inference Capacity Index (GB300e)` | number | none | Epoch AI field, kept exactly as published; not used by this app |

## Processed files the app reads

### `data/processed/global_dc_electricity.csv`

Data-centre electricity in TWh and as a share of demand for World, United States, China and Rest of world, plus the IEA 2030 projection.

- **Dataset ID:** `global_dc_electricity` (owner: Yajat)
- **Source:** Our World in Data, based on IEA (2025, 2026) and Ember (2026), *Share of total electricity demand used by data centers*; Our World in Data, based on Ember (2026), *Electricity demand*; International Energy Agency, *Key Questions on Energy and AI (executive summary)*
- **URL:** https://ourworldindata.org/grapher/data-centers-share-electricity-demand; https://ourworldindata.org/grapher/electricity-demand; https://www.iea.org/reports/key-questions-on-energy-and-ai/executive-summary
- **Licence:** CC BY 4.0 (Our World in Data processing); underlying IEA data under IEA terms; CC BY 4.0; IEA terms of use (figures quoted with attribution)
- **Primary key:** `entity`, `year`
- **Time coverage:** 2020 and 2023-2025 (actual); 2030 (World projection only)
- **Latest observation:** 2025
- **Transform:** `scripts/build_global.py` from `owid_dc_share`, `owid_ember_demand`, `iea_2026_key_numbers`
  1. Keep World, United States and China rows from both OWID files and inner-join on Entity and Year.
  2. dc_twh = share (%) / 100 x Electricity demand (TWh).
  3. Rest of world = World minus United States minus China (TWh); its share = dc_twh / demand_twh x 100.
  4. Add the World 2030 projection (950 TWh, 3%) from the IEA manual file.
  5. Stop if World 2025 differs from the IEA's 485 TWh by 2 TWh or more, or 2024-25 growth from 17% by 1.5 points.

| Column | Type | Unit | Description |
|---|---|---|---|
| `entity` | string | none | World, United States, China or Rest of world |
| `year` | integer | year | Calendar year |
| `kind` | string | none | actual (IEA estimate) or projection (IEA 2026 base case) |
| `dc_share_pct` | number | % | Data-centre share of electricity demand |
| `demand_twh` | number | TWh | Total electricity demand; empty for the projection row |
| `dc_twh` | number | TWh | Data-centre electricity use |
| `method` | string | none | How the row was produced |

### `data/processed/global_growth_index.csv`

World data-centre electricity and world electricity demand, each indexed to 2020 = 100.

- **Dataset ID:** `global_growth_index` (owner: Yajat)
- **Source:** Our World in Data, based on IEA (2025, 2026) and Ember (2026), *Share of total electricity demand used by data centers*; Our World in Data, based on Ember (2026), *Electricity demand*
- **URL:** https://ourworldindata.org/grapher/data-centers-share-electricity-demand; https://ourworldindata.org/grapher/electricity-demand
- **Licence:** CC BY 4.0 (Our World in Data processing); underlying IEA data under IEA terms; CC BY 4.0
- **Primary key:** `year`, `series`
- **Time coverage:** 2020 and 2023-2025
- **Latest observation:** 2025
- **Transform:** `scripts/build_global.py` from `owid_dc_share`, `owid_ember_demand`
  1. Take the World rows of global_dc_electricity (actual only).
  2. index_2020 = value / value in 2020 x 100, separately for each series.

| Column | Type | Unit | Description |
|---|---|---|---|
| `year` | integer | year | Calendar year |
| `series` | string | none | Data-centre electricity or All electricity demand |
| `twh` | number | TWh | Value of the series in that year |
| `index_2020` | number | index (2020 = 100) | twh / twh in 2020 x 100 |

### `data/processed/global_comparisons.csv`

World data-centre electricity in 2025 next to whole countries' electricity demand.

- **Dataset ID:** `global_comparisons` (owner: Yajat)
- **Source:** Our World in Data, based on IEA (2025, 2026) and Ember (2026), *Share of total electricity demand used by data centers*; Our World in Data, based on Ember (2026), *Electricity demand*
- **URL:** https://ourworldindata.org/grapher/data-centers-share-electricity-demand; https://ourworldindata.org/grapher/electricity-demand
- **Licence:** CC BY 4.0 (Our World in Data processing); underlying IEA data under IEA terms; CC BY 4.0
- **Primary key:** `entity`, `year`
- **Time coverage:** 2025
- **Latest observation:** 2025
- **Transform:** `scripts/build_global.py` from `owid_dc_share`, `owid_ember_demand`
  1. Take Australia, United Kingdom, France and Germany 2025 demand from the Ember file.
  2. ratio_dc_to_country = World 2025 data-centre TWh / country demand TWh.

| Column | Type | Unit | Description |
|---|---|---|---|
| `entity` | string | none | Comparison country |
| `year` | integer | year | Calendar year |
| `demand_twh` | number | TWh | The country's total electricity demand |
| `world_dc_twh` | number | TWh | World data-centre electricity use |
| `ratio_dc_to_country` | number | ratio | world_dc_twh / demand_twh |

### `data/processed/water_google.csv`

Google's reported 2025 water figures with plain-English labels, read by the Water page.

- **Dataset ID:** `water_google` (owner: Akil)
- **Source:** Google, *Environmental Report 2026*
- **URL:** https://sustainability.google/files/google-2026-environmental-report.pdf
- **Licence:** Company report (figures quoted with attribution)
- **Primary key:** `metric`, `year`
- **Time coverage:** 2025
- **Latest observation:** 2025
- **Transform:** `scripts/build_water.py` from `google_2026_water_numbers`
  1. Read the five reported numbers from the manual file.
  2. Add a plain-English label to each. No value is changed.
  3. The page computes The Dalles share = The Dalles gallons / total gallons x 100.

| Column | Type | Unit | Description |
|---|---|---|---|
| `metric` | string | none | Machine name of the measure |
| `label` | string | none | Plain-English name of the measure |
| `year` | integer | year | Year the number refers to |
| `value` | number | see unit column | The reported number, unchanged |
| `unit` | string | none | Unit of value (billion_gallons or %) |

### `data/processed/compute_vs_efficiency.csv`

Record-to-date training compute of the largest AI model and FP32 efficiency of the best chip, by year, each indexed to 2012 = 1.

- **Dataset ID:** `compute_vs_efficiency` (owner: Niki)
- **Source:** Epoch AI, *Notable AI Models*; Epoch AI, *Machine Learning Hardware*
- **URL:** https://epoch.ai/data/notable-ai-models; https://epoch.ai/data/machine-learning-hardware
- **Licence:** CC BY 4.0; CC BY 4.0
- **Primary key:** `series`, `year`
- **Time coverage:** 2012-2025
- **Latest observation:** 2025
- **Transform:** `scripts/build_compute.py` from `epoch_notable_ai_models`, `epoch_ml_hardware`
  1. Models: keep rows with a publication date and a positive Training compute (FLOP).
  2. Chips: keep rows with a release date, FP32 performance and TDP; efficiency = FP32 FLOP/s / TDP W.
  3. For each year keep the best value released up to and including that year, so neither series falls.
  4. Index each series to its 2012 value = 1.
  5. Stop if a record falls or either series fails to grow.

| Column | Type | Unit | Description |
|---|---|---|---|
| `year` | integer | year | Calendar year |
| `series` | string | none | Training compute of the largest model, or Efficiency of the best chip (FP32) |
| `value` | number | see unit column | Record value released up to and including this year |
| `unit` | string | none | Unit of value (FLOP or FLOP/s per W) |
| `record_holder` | string | none | Model or chip that holds the record |
| `record_organization` | string | none | Developer or manufacturer of the record holder |
| `record_year` | integer | year | Year the record holder was released |
| `index_2012` | number | index (2012 = 1) | value divided by the series' 2012 value |

### `data/processed/compute_growth_summary.csv`

Total multiple, average yearly growth and doubling time of each series in compute_vs_efficiency, 2012 to 2025.

- **Dataset ID:** `compute_growth_summary` (owner: Niki)
- **Source:** Epoch AI, *Notable AI Models*; Epoch AI, *Machine Learning Hardware*
- **URL:** https://epoch.ai/data/notable-ai-models; https://epoch.ai/data/machine-learning-hardware
- **Licence:** CC BY 4.0; CC BY 4.0
- **Primary key:** `series`
- **Time coverage:** 2012-2025
- **Latest observation:** 2025
- **Transform:** `scripts/build_compute.py` from `compute_vs_efficiency`
  1. growth_per_year = (end_value / start_value) ^ (1 / (end_year - start_year)).
  2. doubling_time_months = 12 x ln 2 / ln(growth_per_year).

| Column | Type | Unit | Description |
|---|---|---|---|
| `series` | string | none | Series name, as in compute_vs_efficiency |
| `start_year` | integer | year | First year of the comparison |
| `end_year` | integer | year | Last year of the comparison |
| `start_value` | number | FLOP or FLOP/s per W | Record value in start_year |
| `end_value` | number | FLOP or FLOP/s per W | Record value in end_year |
| `total_multiple` | number | times | end_value / start_value |
| `growth_per_year` | number | times per year | total_multiple ^ (1 / years) |
| `doubling_time_months` | number | months | 12 x ln 2 / ln(growth_per_year) |
