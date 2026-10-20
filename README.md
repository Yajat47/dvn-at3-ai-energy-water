# AI's energy and water footprint: a global problem, or a local one?

DVN 36104 Assignment 3 group data narrative, built with Streamlit.

- **Live app:** https://dvn-at3-ai-energy-water.streamlit.app
- **Repository:** https://github.com/Yajat47/dvn-at3-ai-energy-water

## Question

**Question:** Is AI's energy and water footprint a global problem, or a local one?

It is arguable because the same data supports both answers. Measured against the whole world, data centres use a small slice of electricity. Measured against the grids and water catchments they cluster in, that slice can be large.

## Persona

**Persona:** Daniel, an infrastructure planner at a Western Sydney council (fictional). **Decision the app serves:** what Daniel advises councillors when data-centre development applications come in, either to treat them as a real risk to local electricity and water supply, or as a headline that looks bigger than it is.

## User stories

1. As an infrastructure planner at a Western Sydney council, I want to see how much electricity data centres use worldwide and how fast that is growing, so that I can judge whether AI's footprint is a world-scale problem or a small share of global demand.
   *Walk-through:* Home, then **1. Global scale**: the four number cards, the 2020-2030 chart (switch between TWh and share), the growth index and the regional breakdown.
2. As an infrastructure planner at a Western Sydney council, I want to compare the data-centre share of electricity and water in the places they cluster with the global share, so that I can judge how heavily a cluster like Western Sydney could load the local grid and catchment.
   *Walk-through:* **2. Where it lands**, then **4. Water**.
3. As an infrastructure planner at a Western Sydney council, I want to see whether efficiency gains are keeping pace with the growth in AI compute, so that I know whether to plan for data-centre demand that keeps rising or one that levels off.
   *Walk-through:* **3. Compute vs efficiency**, then the 2030 projection on **1. Global scale**.

The same three stories appear on the app's Home page with links (`USER_STORIES` in `utils/story.py`). Keep the two in step.

## Who owns what

| Page | File | Owner |
|---|---|---|
| Home | `views/home.py` | Yajat |
| 1. Global scale | `views/global_scale.py` | Yajat |
| 2. Where it lands | `views/where_it_lands.py` | Member A |
| 3. Compute vs efficiency | `views/compute_vs_efficiency.py` | Member B |
| 4. Water | `views/water.py` | Member C |
| Sources and method | `views/sources.py` | Yajat |

## Portfolio documents

| Document | What it is |
|---|---|
| `data/DATA_DICTIONARY.md` | Every dataset: source, URL, licence, columns and units, primary key, time coverage, latest observation, transform. Generated from `data/data_dictionary.yml`. |
| `docs/AI_PROVENANCE.md` | AI provenance matrix: one row per substantive AI use, at least one per member. |
| `DISCLOSURE.md` | Data and AI disclosure statement. |
| `docs/PART2_CHECKLIST.md` | The 30 marking checks, how we meet each one, and who owns it. |
| `docs/design-log.md` | Design decisions per chart. |

## Run it locally

```bash
python3.11 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

## Data package

```
data/samples/                source samples, exactly as downloaded (never edited)
data/samples/manual/         numbers copied from report text, with the sentence beside each one
data/processed/              files the app reads, produced only by scripts/build_*.py
data/data_dictionary.yml     the dictionary: edit this
data/DATA_DICTIONARY.md      the same dictionary as a readable page (generated)
```

```bash
python scripts/fetch_sources.py   # live mode: re-download the source samples
python scripts/build_all.py       # offline mode: regenerate data/processed/ from the samples, render the dictionary
python scripts/check_package.py   # check the package, docs and app against the rubric
```

`check_package.py` rebuilds every processed file in a throwaway copy from the samples alone and checks the result matches what is committed. It also checks the dictionary against the files, the README, the provenance matrix and the disclosure, then opens every page of the app and tests the charts and controls. The GitHub Action runs it on every push and pull request.

## How we work

1. **Branch per person:** `git checkout -b <name>/<page>`.
2. **Edit your own page, script and data.** Shared files (`utils/`, `app.py`, `data/data_dictionary.yml`, `docs/AI_PROVENANCE.md`, `DISCLOSURE.md`): add your part and say so in the PR.
3. **Run `python scripts/build_all.py` then `python scripts/check_package.py` before opening a PR.** No new FAILs.
4. **Open a pull request into `main`.** Yajat reviews and merges; Streamlit redeploys from `main`.

## Rules

**Data**
- Every number on screen is computed from a file in `data/`. Never type a number into a page.
- Source samples are never edited. A transform lives in `scripts/build_<page>.py`.
- Every file in `data/` has an entry in `data/data_dictionary.yml`, with type, unit and description for every column.
- Put a `trace(...)` box under every chart.

**Charts**
- Every chart has a title stating the finding and a caption with the unit, the baseline and the years covered.
- Every axis and every legend has a title with units: `style(fig, x_title=..., y_title=..., legend_title=...)`.
- Every value is readable without hovering: label the points or bars.
- Colours only from `utils/theme.py`. Solid for actual data, dashed for projections. No dual y-axes.
- A filter that can be emptied shows a message, not an error or a blank chart.

## Deploying and submitting

Streamlit Community Cloud deploys `main` (entry point `app.py`, Python 3.11). The assessed version is the release tag listed in the submission PDF. The free tier sleeps when idle, so open the app before anyone times it.
