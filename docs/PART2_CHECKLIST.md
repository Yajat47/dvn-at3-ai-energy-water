# Part 2 checklist (due Fri 20 Nov 2026, 11:59pm)

Thirty pass/fail checks, one mark each. `python scripts/check_package.py` tests the ones marked **auto**; the rest need a person. "Status" is as of 27 Oct 2026 (release `v1.1`).

## Timeline

| Date | Milestone |
|---|---|
| Tue 27 Oct | Each member: source samples in `data/samples/`, dictionary entries, a build script and a first chart, opened as a PR |
| Fri 6 Nov | Every page complete; `check_package.py` has no FAILs |
| Tue 10 Nov | Group review of the manual checks below at 1366x768; Home answer updated with pages 2-4 evidence |
| Fri 13 Nov | Content freeze. Provenance rows and disclosure statements final |
| Tue 17 Nov | Tag `v1.0`; confirm the deployed app runs that commit |
| Wed 18 Nov | Submission PDF; peer contribution factors agreed |
| Fri 20 Nov | Submit by 6pm; open the app so it is awake |

## The 30 checks

| # | Check | How we meet it | Owner | Test | Status |
|---|---|---|---|---|---|
| 1 | README states the question in one sentence | `**Question:**` line in README | Yajat | auto | Pass |
| 2 | Question on the app's opening screen | Home page heading | Yajat | auto | Pass |
| 3 | Question is arguable | 1.5% of world electricity vs much higher local shares; stated on Home | All | manual | Pass |
| 4 | README names persona and the decision | `**Persona:**` with "Decision the app serves" | Yajat | auto | Pass |
| 5 | Three as-a / I-want / so-that stories | README "User stories" | Yajat | auto | Pass |
| 6 | Each story walkable in the app | Home links each story to its pages | All | manual | Stories 1 and 2 pass; **story 3 fails until page 3 is built** |
| 7 | Every number in or computed from the data package | Numbers computed in code from `data/`; trace box under each chart | All | manual | Home and pages 1, 2, 4 pass; page 3 to come |
| 8 | App states an answer in text | Home "Our answer" | Yajat (+ team update) | auto | Pass; the answer cites pages 1, 2 and 4 |
| 9 | App states what the data cannot show | Home "What this data cannot show" (`LIMITS` in `utils/story.py`) | All add their limits | auto | Pass |
| 10 | Units, baselines, time coverage wherever numbers are compared | Chart captions and number-card captions | All | manual | Pages 1, 2, 4 pass |
| 11 | On-screen claims stay within the data | No causal claims or extrapolation beyond the files | All | manual | Pages 1, 2 pass; **page 4 cites two report claims that are not in the data package** |
| 12 | Every chart has a title or caption saying what it shows | `####` title stating the finding plus `st.caption` | All | manual | Pages 1, 2, 4 pass |
| 13 | At least four charts | Page 1 has 3; each other page adds at least 1 | All | auto | Pass (5 charts) |
| 14 | At least three Visual Vocabulary families | See the family plan below | All | manual | Pass: change over time, part-to-whole, magnitude |
| 15 | Form matches task | Design log entry per chart | All | manual | Pages 1, 2, 4 pass |
| 16 | Every axis and legend labelled with units | `style(fig, x_title=, y_title=, legend_title=)` | All | auto | Pass |
| 17 | Every value readable without hovering | Text labels on every point or bar | All | auto (warning) | Pass |
| 18 | Colours survive a CVD check | Only `utils/theme.py` colours; validator passed (below) | All | auto | Pass |
| 19 | Deployed URL loads in under 5 s | Light pages; app opened before marking | Yajat | manual | **At risk:** about 8 s on a first visit in a fresh browser (Streamlit Cloud's loader takes about 4.4 s before the app starts), about 3 s on a repeat visit |
| 20 | Opens on something true about the whole dataset | Home "Across the whole dataset, in 2025" cards | Yajat | manual | Pass |
| 21 | Two interactions change the view in about a second | Page 1: TWh/share toggle, region filter | All | auto | Pass |
| 22 | Empty filter shows a message | Page 1 region filter; every multiselect needs one | All | auto | Pass |
| 23 | Works at 1366x768, vertical scroll only | Checked in browser | All | manual | Pass on every page (Sources tables fixed 27 Oct) |
| 24 | Sources and last refresh on screen | Footer on every page from the dictionary | Yajat | auto | Pass |
| 25 | Data folder with samples and processed files | `data/samples/`, `data/processed/` | All | auto | Pass |
| 26 | Data dictionary covers every dataset | `data/data_dictionary.yml` and generated `DATA_DICTIONARY.md` | All | auto | **Fail until the four page 3 data files have entries** |
| 27 | Commit hash or tag resolves and the app runs | Release tag; checker opens every page | Yajat | auto + manual | Tag `v1.1`; `main` matches it |
| 28 | Provenance row from every member, verification that could fail | `docs/AI_PROVENANCE.md` | **Each member** | auto | **Fail until Siddharth and Niki add rows** |
| 29 | Data and AI disclosure statement | `DISCLOSURE.md` | All add their AI section | auto | Pass |
| 30 | Processed files regenerate from samples | `scripts/build_all.py`; checker rebuilds in a clean copy | All | auto | Pass |

## Chart family plan (check 14)

Families from the FT Visual Vocabulary. Three are needed across the app; this plan gives five.

| Page | Chart | Family |
|---|---|---|
| 1. Global scale | Data-centre electricity 2020-2030 (line) | Change over time |
| 1. Global scale | Growth index 2020 = 100 (line) | Change over time |
| 1. Global scale | Regional breakdown (stacked bar) | Part-to-whole |
| 2. Where it lands | Data-centre share by place, sorted (bar or dot plot) | **Ranking** |
| 3. Compute vs efficiency | Training compute vs hardware efficiency (scatter, log scale) | **Correlation** |
| 4. Water | Data-centre water use by year or operator (bar), or a map of sites vs water stress | **Magnitude** or **Spatial** |

## Colour check (check 18)

The categorical slots in `utils/theme.py` (`#2a78d6`, `#eb6834`, `#1baf7a`) passed a colour-vision-deficiency validator on 20 Oct 2026, all pairs: worst CVD separation delta E 9.2 (target 8 or more), worst normal-vision delta E 24.0. Grey `#b4b2a9` is only used for context series, which are also labelled. Use only these colours, and label series directly so colour is never the only cue.

## Every page owner, before your PR

- [ ] Source files in `data/samples/` (unchanged) and an entry for each in `data/data_dictionary.yml`
- [ ] `scripts/build_<page>.py` writing your `data/processed/` files, and an entry for each
- [ ] At least one chart, from your family in the plan above
- [ ] Each chart: finding as the title, caption with unit, baseline and years, axis and legend titles with units, labelled values
- [ ] At least one control that changes the chart; a multiselect that shows a message when emptied
- [ ] A `trace(...)` box under every chart
- [ ] Your limits added to `LIMITS` in `utils/story.py`
- [ ] Your row(s) in `docs/AI_PROVENANCE.md` and your section in `DISCLOSURE.md`
- [ ] Your design decision in `docs/design-log.md`
- [ ] `python scripts/build_all.py` then `python scripts/check_package.py`: no new FAILs
