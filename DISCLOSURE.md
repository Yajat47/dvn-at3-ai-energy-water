# Data and AI disclosure statement

## Data

- **What we used.** Only public, citable sources, listed with their URLs, licences and retrieval dates in `data/DATA_DICTIONARY.md`: the International Energy Agency (*Key Questions on Energy and AI*, 2026), Our World in Data (data-centre share of electricity, based on IEA and Ember), and Ember electricity demand via Our World in Data. Page owners add their sources to the dictionary.
- **How we used it.** Source files are stored unchanged in `data/samples/`. Numbers taken from report text are typed into `data/samples/manual/` with the original sentence beside each one. Every processed file in `data/processed/` is produced by a script in `scripts/`, and `python scripts/build_all.py` regenerates all of them from the samples.
- **Licences.** Our World in Data and Ember data are CC BY 4.0. IEA figures are quoted with attribution under the IEA's terms of use. We redistribute only what those terms allow.
- **Personal data.** None. All data is aggregated at country, region or company level.
- **Limits.** What the data cannot show is stated on the app's Home page, for example that most data-centre electricity figures are IEA model estimates rather than measurements.

## AI

Every substantive AI use is a row in the AI provenance matrix, `docs/AI_PROVENANCE.md`: the artefact, who, the tool, what was asked, what came back, how it was verified and the outcome. Each member's statement follows.

### Yajat: Home, 1. Global scale, Sources and method, repo setup

**Tool:** Claude (Anthropic), used through Claude Code, 20 October 2026 onwards.

**What I used it for**

- **Finding sources.** Searching for recent, citable data on AI's electricity and water use (IEA *Key Questions on Energy and AI* 2026, Our World in Data, Ember, CSO Ireland, AEMO 2026 ESOO, Sydney water reporting), summarised in `docs/research-brief.md`.
- **Setting up the repo.** Project structure, shared chart theme, the "Where does this number come from?" trace box, page template, placeholder pages for teammates, and creating the GitHub repo and Streamlit deployment.
- **Code for my pages.** The data pipeline (`scripts/fetch_sources.py`, `scripts/build_global.py`, `scripts/build_all.py`) and the Home, Global scale and Sources pages.
- **Part 2 package.** The data dictionary, the package checker (`scripts/check_package.py`) and its GitHub Action, and fixes to my page for the marking checks.
- **Documentation.** README, this statement's structure, `docs/design-log.md`, `docs/research-brief.md`, `docs/PART2_CHECKLIST.md`.
- **Story.** It suggested the wording of the group question and the persona. I had the persona renamed.
- **My Part 1 recording.** A rehearsal script, a transcript of my recording, and trimming the recording to under five minutes.

Commits made with Claude are marked `Co-Authored-By: Claude` in the git history.

**How I checked it**

I did not take the output on trust.

1. **Recalculated the headline number by hand.** 1.5264845 / 100 x 31,772.35 = 485.0 TWh, using the World 2025 rows of the two source samples.
2. **Went to the IEA report myself.** Found the sentence "...from 485 TWh in 2025 to 950 TWh in 2030" in *Key Questions on Energy and AI* (2026), which matches the app.
3. **Ran the build check.** `scripts/build_global.py` stops if our 2025 figure differs from the IEA's 485 TWh by 2 TWh or more, or if 2024-25 growth drifts from the IEA's 17%. It printed `check ok`.
4. **Checked publication dates.** Confirmed the figures come from current releases (IEA 2026 report, OWID and Ember data updated in 2026), not old or invented numbers.
5. **Dropped untraceable claims.** Two widely quoted figures (data centres as "17% of global electricity demand growth in 2025", and "IEA projects 1,000 TWh by 2026") could not be traced to a primary source, so they are not in the app.
6. **Pushed back on complexity.** I flagged coding directions that added more complexity than the page needed.

### Siddharth Guruswamy: 2. Where it lands

_To be added by Siddharth._

### Niki Miyake: 3. Compute vs efficiency

_To be added by Niki._

### Akil Venkateshkumar: 4. Water

**Tool:** Claude (Anthropic), used through the Claude chat app, October 2026.

**What I used it for**

- **Code for my page.** The Water page (`views/water.py`), its build script (`scripts/build_water.py`) and the manual data file (`data/samples/manual/google_2026_water.csv`).
- **Extracting figures.** It read the Google 2026 Environmental Report PDF and pulled out the water numbers.
- **Documentation.** My data dictionary entries, provenance row and design-log entry.

**How I checked it**

1. I opened the report PDF and checked each number in the manual file against its page.
2. I recalculated The Dalles share by hand: 0.469 / 10.9 x 100 = 4.3%.
3. I ran `python scripts/build_all.py` and `python scripts/check_package.py` and fixed anything flagged.
