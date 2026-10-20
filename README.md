# AI's energy and water footprint: a global problem, or a local one?

DVN 36104 Assignment 3 group data narrative, built with Streamlit.

- **Live app:** _add the Streamlit URL here once deployed_
- **Question:** Is AI's energy and water footprint a global problem, or a local one?
- **Persona:** Priya, an infrastructure planner at a Western Sydney council assessing data-centre development applications (fictional).

## Who owns what

| Page | File | Owner | Persona question it answers |
|---|---|---|---|
| Home | `views/home.py` | Yajat | The question, persona and story so far |
| 1. Global scale | `views/global_scale.py` | Yajat | How big is AI's footprint, and how fast is it growing? |
| 2. Where it lands | `views/where_it_lands.py` | Member A | Where does that load actually land? |
| 3. Compute vs efficiency | `views/compute_vs_efficiency.py` | Member B | Will efficiency gains cancel out the growth? |
| 4. Water | `views/water.py` | Member C | What does it mean for water, not just power? |
| Sources and method | `views/sources.py` | Yajat | Where every number comes from |

Replace "Member A/B/C" here and in `utils/story.py` with real names.

## Run it locally

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

## Repo layout

```
app.py                  registers every page (you should not need to edit it)
views/                  one file per page; each person edits only their own
views/_page_template.py copy this to start your page
utils/story.py          question, persona, team names, page status
utils/theme.py          shared colours and chart style
utils/trace.py          the "Where does this number come from?" box
utils/data.py           loaders for raw and processed files
data/raw/               downloads exactly as published, never edited
data/raw/manual/        numbers copied from report text, with the original sentence
data/processed/         outputs of scripts/, read by the pages
scripts/                one build script per page: raw -> processed
sources.csv             one row per source
docs/design-log.md      each person's design decision, for the recording
docs/research-brief.md  checked facts and sources for the whole narrative
```

## How we work

1. **Branch per person.** `git checkout -b <name>/<page>`, for example `alex/where-it-lands`.
2. **Edit only your own page file and your own scripts and data.** This keeps merge conflicts close to zero.
3. **Open a pull request into `main`.** Yajat reviews and merges. Streamlit Cloud redeploys from `main` automatically.
4. **Before opening a PR:** run `streamlit run app.py` and click through every page. No red errors.
5. Shared files (`utils/`, `app.py`, `sources.csv`): small changes are fine. Mention them in the PR description.

## Data rules

- Every number on screen comes from a file in this repo. Compute it in code; never type it into the page.
- Raw downloads go in `data/raw/` and are never edited. If a source updates, re-download and rebuild.
- A number copied from report text goes in `data/raw/manual/` with a `quote` column holding the sentence word for word.
- Every transformation lives in `scripts/build_<page>.py`. Add a check against a published figure where you can (see `scripts/build_global.py`).
- Add a row to `sources.csv` for every source: id, title, publisher, URL, licence, file, date retrieved, owner.
- Put a `trace(...)` box under every chart. It is what lets each of us trace a number live in the recording.
- Keep files under 50 MB. If a source is bigger, trim it in a script and say so in `sources.csv`.

## Chart rules

- Use colours from `utils/theme.py`: one colour for the series that matters, grey for context.
- Actual data is solid, projections are dashed. Nothing else is dashed.
- No dual y-axes. Index to a common base, or use two charts.
- No pies or donuts for close values.
- Chart titles state the finding ("Two countries use 70% of it"), not just the topic.

## Rebuild the data

```bash
python scripts/fetch_raw.py      # re-download raw files
python scripts/build_global.py   # page 1 tables (stops if numbers drift from the IEA's)
```

## Deploying

The app is on Streamlit Community Cloud, deployed from `main` with entry point `app.py` and Python 3.11. The free tier puts the app to sleep when idle, so open it a few minutes before recording and wait for it to wake.
