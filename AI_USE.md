# AI use

---

## Yajat: Home, 1. Global scale, Sources and method, repo setup

**Tool:** Claude (Anthropic), used through Claude Code, 20 October 2026.

### What I used it for

- **Finding sources.** Searching for recent, citable data on AI's electricity and water use (IEA *Key Questions on Energy and AI* 2026, Our World in Data, Ember, CSO Ireland, AEMO 2026 ESOO, Sydney water reporting), summarised in `docs/research-brief.md`.
- **Setting up the repo.** Project structure, shared chart theme, the "Where does this number come from?" trace box, `sources.csv`, page template, placeholder pages for teammates, and creating the GitHub repo and Streamlit deployment.
- **Code for my page.** The data pipeline (`scripts/fetch_raw.py`, `scripts/build_global.py`) and the Home, Global scale and Sources pages.
- **Documentation.** README, `docs/design-log.md`, `docs/research-brief.md`.
- **Story.** It suggested the wording of the group question and the persona. I had the persona renamed.
- **My recording.** A rehearsal script, a transcript of my recording, and trimming the recording to under five minutes.

Commits made with Claude are marked `Co-Authored-By: Claude` in the git history.

### How I checked it

I did not take the output on trust.

1. **Recalculated the headline number by hand.** 1.5264845 / 100 x 31,772.35 = 485.0 TWh, using the World 2025 rows in the two raw files (line 37 of `owid_data_centers_share_electricity_demand.csv`, line 6304 of `owid_ember_electricity_demand.csv`).
2. **Went to the IEA report myself.** Found the sentence "...from 485 TWh in 2025 to 950 TWh in 2030" in *Key Questions on Energy and AI* (2026), which matches the app.
3. **Ran the build check.** `python scripts/build_global.py` stops if our 2025 figure differs from the IEA's 485 TWh by 2 TWh or more, or if 2024-25 growth drifts from the IEA's 17%. It printed `check ok`.
4. **Checked publication dates.** Confirmed the figures come from current releases (IEA 2026 report, OWID and Ember data updated in 2026), not old or invented numbers.
5. **Dropped untraceable claims.** Two widely quoted figures (data centres as "17% of global electricity demand growth in 2025", and "IEA projects 1,000 TWh by 2026") could not be traced to a primary source, so they are not in the app.
6. **Pushed back on complexity.** I flagged coding directions that added more complexity than the page needed.

---

## Member A: 2. Where it lands

_To be added by Member A._

## Member B: 3. Compute vs efficiency

_To be added by Member B._

## Member C: 4. Water

_To be added by Member C._
