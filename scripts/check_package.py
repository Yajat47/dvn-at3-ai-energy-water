"""Check the repo against the mechanical parts of the A3 Part 2 rubric.

Run from the repo root:  python scripts/check_package.py [--pending 13,28]

--pending lists rubric numbers whose FAILs are reported as WARN, for checks that are waiting on work in
progress (the GitHub Action uses it until every member has contributed; remove it from the workflow
before the 6 Nov milestone).

Each line reports PASS, FAIL, WARN or MANUAL with the rubric check number. FAIL exits with code 1, so
the GitHub Action blocks a pull request that breaks the data package or the app. MANUAL items need a
person to look; the checklist in docs/PART2_CHECKLIST.md says how.
"""

import ast
import json
import math
import re
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path

import pandas as pd
import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))

RESULTS: list[tuple[str, str, str, str]] = []  # (status, rubric no, check, detail)
DATA_EXT = {".csv", ".json", ".parquet"}
PAGES = [
    "views/home.py",
    "views/global_scale.py",
    "views/where_it_lands.py",
    "views/compute_vs_efficiency.py",
    "views/water.py",
    "views/sources.py",
]


def record(status: str, no: str, check: str, detail: str = "") -> None:
    RESULTS.append((status, no, check, detail))


def ok(cond: bool, no: str, check: str, detail_fail: str = "", detail_pass: str = "") -> bool:
    record("PASS" if cond else "FAIL", no, check, detail_pass if cond else detail_fail)
    return cond


def read(path: Path) -> pd.DataFrame:
    if path.suffix == ".csv":
        return pd.read_csv(path, keep_default_na=False, na_values=[""])
    if path.suffix == ".json":
        return pd.read_json(path)
    return pd.read_parquet(path)


# ---------------------------------------------------------------- data package (25, 26, 30)
def check_data_package() -> None:
    dict_path = ROOT / "data" / "data_dictionary.yml"
    if not ok(dict_path.exists(), "26", "data/data_dictionary.yml exists"):
        return
    d = yaml.safe_load(dict_path.read_text(encoding="utf-8"))
    sources = {s.get("id"): s for s in d.get("sources", [])}
    datasets = d.get("datasets", [])

    samples = [p for p in (ROOT / "data" / "samples").rglob("*") if p.suffix in DATA_EXT]
    processed = [p for p in (ROOT / "data" / "processed").rglob("*") if p.suffix in DATA_EXT]
    ok(bool(samples) and bool(processed), "25", "data/ holds source samples and processed files",
       f"{len(samples)} sample files, {len(processed)} processed files")

    # Every processed file a page reads must exist.
    read_by_app = set()
    for page in (ROOT / "views").glob("*.py"):
        read_by_app |= set(re.findall(r'data\.processed\(\s*"([^"]+)"\s*\)', page.read_text(encoding="utf-8")))
    read_by_app.discard("TODO_your_processed_file")
    missing = sorted(n for n in read_by_app if not (ROOT / "data" / "processed" / f"{n}.csv").exists())
    ok(not missing, "25", "every processed file the app reads is in data/processed/", f"missing: {missing}",
       f"{len(read_by_app)} files read by pages")

    # Sources: every field present.
    need_src = ["id", "title", "publisher", "url", "licence", "retrieved"]
    bad_src = [f"{s.get('id')}: {k}" for s in sources.values() for k in need_src if not str(s.get(k, "")).strip()]
    ok(not bad_src, "26", "every source has id, title, publisher, URL, licence, retrieved date", "; ".join(bad_src))

    # Every data file is described.
    described = {ds.get("path") for ds in datasets} | {ds.get("metadata_file") for ds in datasets}
    all_files = [p.relative_to(ROOT).as_posix() for p in samples + processed]
    undescribed = [f for f in all_files if f not in described]
    ok(not undescribed, "26", "every data file has a dictionary entry", f"not in dictionary: {undescribed}",
       f"{len(all_files)} files")

    need_ds = ["id", "role", "path", "format", "source_ids", "description", "primary_key", "time_coverage",
               "latest_observation", "columns", "transform", "owner"]
    problems = []
    for ds in datasets:
        name = ds.get("id", ds.get("path"))
        for k in need_ds:
            if ds.get(k) in (None, "", [], {}):
                problems.append(f"{name}: missing {k}")
        for sid in ds.get("source_ids", []):
            if sid not in sources:
                problems.append(f"{name}: unknown source {sid}")
        path = ROOT / ds.get("path", "")
        if not path.exists():
            problems.append(f"{name}: file not found")
            continue
        df = read(path)
        cols = ds.get("columns", {})
        for c, spec in cols.items():
            if not isinstance(spec, dict) or set(spec) != {"type", "unit", "description"} or not all(
                str(v).strip() for v in spec.values()
            ):
                problems.append(f"{name}: column '{c}' needs exactly type, unit and description")
        if set(cols) != set(df.columns):
            problems.append(f"{name}: columns differ from file (dictionary only: {sorted(set(cols) - set(df.columns))}, "
                            f"file only: {sorted(set(df.columns) - set(cols))})")
        pk = ds.get("primary_key", [])
        if pk and all(k in df.columns for k in pk):
            if df.duplicated(pk).any() or df[pk].isna().any().any():
                problems.append(f"{name}: primary key {pk} is not unique and non-empty")
        tc = ds.get("time_column")
        if tc and tc in df.columns:
            obs = df.query(ds["observation_filter"]) if ds.get("observation_filter") else df
            latest = obs[tc].max()
            if str(latest) != str(ds.get("latest_observation")):
                problems.append(f"{name}: latest_observation {ds.get('latest_observation')} but data says {latest}")
        if ds.get("role") == "processed":
            t = ds.get("transform", {})
            if not isinstance(t, dict) or not (ROOT / t.get("script", "")).exists() or not t.get("steps"):
                problems.append(f"{name}: processed files need transform.script (existing), inputs and steps")
            else:
                ids = {x.get("id") for x in datasets}
                problems += [f"{name}: unknown input {i}" for i in t.get("inputs", []) if i not in ids]
    ok(not problems, "26", "dictionary entries complete and match the files (columns, units, key, latest observation)",
       "; ".join(problems[:8]) + (" ..." if len(problems) > 8 else ""), f"{len(datasets)} datasets")

    from build_all import render_dictionary_text

    md = ROOT / "data" / "DATA_DICTIONARY.md"
    ok(md.exists() and md.read_text(encoding="utf-8") == render_dictionary_text(), "26",
       "data/DATA_DICTIONARY.md is up to date", "run: python scripts/build_all.py")

    check_regeneration(datasets)


def frames_equal(a: pd.DataFrame, b: pd.DataFrame) -> bool:
    if list(a.columns) != list(b.columns) or len(a) != len(b):
        return False
    a, b = a.reset_index(drop=True), b.reset_index(drop=True)
    for c in a.columns:
        for x, y in zip(a[c], b[c]):
            if pd.isna(x) and pd.isna(y):
                continue
            if isinstance(x, (int, float)) and isinstance(y, (int, float)):
                if not math.isclose(float(x), float(y), rel_tol=1e-9, abs_tol=1e-9):
                    return False
            elif str(x) != str(y):
                return False
    return True


def check_regeneration(datasets: list[dict]) -> None:
    """Rebuild every processed file in a throwaway copy, from the samples only, and compare."""
    outputs = [ds["path"] for ds in datasets if ds.get("role") == "processed"]
    with tempfile.TemporaryDirectory() as tmp:
        copy = Path(tmp) / "repo"
        shutil.copytree(ROOT, copy, ignore=shutil.ignore_patterns(".git", ".venv", "venv", "__pycache__"))
        for out in outputs:
            (copy / out).unlink(missing_ok=True)
        sample_hash = {p: p.read_bytes() for p in (copy / "data" / "samples").rglob("*") if p.is_file()}
        t0 = time.time()
        run = subprocess.run([sys.executable, "scripts/build_all.py"], cwd=copy, capture_output=True, text=True,
                             timeout=300)
        took = time.time() - t0
        if not ok(run.returncode == 0, "30", "scripts/build_all.py runs from the samples alone",
                  (run.stderr or run.stdout)[-400:], f"{took:.1f}s"):
            return
        changed = [p.name for p, b in sample_hash.items() if p.read_bytes() != b]
        ok(not changed, "30", "rebuild leaves the source samples untouched", f"changed: {changed}")
        diffs = [o for o in outputs if not (copy / o).exists() or not frames_equal(read(copy / o), read(ROOT / o))]
        ok(not diffs, "30", "processed files regenerate identically from the samples", f"differ: {diffs}",
           f"{len(outputs)} files")


# ---------------------------------------------------------------- docs (1, 4, 5, 28, 29)
def check_docs() -> None:
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    m = re.search(r"\*\*Question:\*\*\s*(.+)", readme)
    q = m.group(1).strip() if m else ""
    one_sentence = bool(q) and q.endswith("?") and len(re.findall(r"[.?!](\s|$)", q)) == 1
    ok(one_sentence, "1", "README states the question in one sentence", "add a line: **Question:** <one sentence>?", q)

    m = re.search(r"\*\*Persona:\*\*(.+?)(\n\n|\n#)", readme, re.S)
    persona = m.group(1) if m else ""
    ok(bool(persona) and re.search(r"decision|decide", persona, re.I) is not None, "4",
       "README names the persona and the decision the app serves", "add **Persona:** ... with the decision it serves")

    stories = re.findall(r"As an? [^,\n]+, I want [^\n]+?, so that [^\n]+", readme)
    ok(len(stories) >= 3, "5", "README lists three as-a / I-want / so-that user stories", f"found {len(stories)}",
       f"found {len(stories)}")

    from utils.story import TEAM

    members = sorted(set(TEAM.values()))
    prov = ROOT / "docs" / "AI_PROVENANCE.md"
    if ok(prov.exists(), "28", "docs/AI_PROVENANCE.md exists"):
        rows = [r for r in prov.read_text(encoding="utf-8").splitlines() if r.startswith("|")]
        header = [c.strip().lower() for c in rows[0].strip("|").split("|")] if rows else []
        need = ["artefact", "who", "tool", "what was asked", "what came back", "how it was verified", "outcome"]
        if ok(header[: len(need)] == need, "28", "provenance matrix has the required columns",
              f"header is {header}"):
            body = [[c.strip() for c in r.strip("|").split("|")] for r in rows[2:]]
            real = [r for r in body if len(r) >= 7 and r[6] and "TODO" not in " ".join(r) and len(r[5]) > 25]
            have = {r[1] for r in real}
            lacking = [m for m in members if m not in have]
            ok(not lacking, "28", "every member owns a provenance row with a verification that could have failed",
               f"no complete row yet for: {lacking}", f"{len(real)} rows")

    disc = ROOT / "DISCLOSURE.md"
    text = disc.read_text(encoding="utf-8") if disc.exists() else ""
    ok(bool(re.search(r"^#+ .*data", text, re.I | re.M)) and bool(re.search(r"^#+ .*\bAI\b", text, re.M)), "29",
       "DISCLOSURE.md has a data section and an AI section", "create DISCLOSURE.md with ## Data and ## AI headings")


# ---------------------------------------------------------------- app (2, 8, 9, 13, 16, 17, 18, 21, 22, 24, 27)
def chart_specs(at) -> list[dict]:
    return [json.loads(c.proto.spec) for c in at.get("plotly_chart")]


def check_app() -> None:
    from streamlit.testing.v1 import AppTest

    from utils.story import QUESTION
    from utils.theme import CONTEXT, SERIES

    at = AppTest.from_file(str(ROOT / "app.py"), default_timeout=60)
    t0 = time.time()
    at.run()
    record("PASS" if time.time() - t0 < 3 else "WARN", "19", "home page renders quickly in a local test",
           f"{time.time() - t0:.2f}s (the deployed URL still needs a manual timing)")
    texts = lambda: " ".join(m.value for m in list(at.markdown) + list(at.title) + list(at.caption))  # noqa: E731
    ok(not at.exception, "27", "home page runs without an error", str([e.value for e in at.exception])[:300])
    ok(QUESTION in texts(), "2", "the question is on the opening screen")
    ok(re.search(r"#+ Our answer", texts()) is not None, "8", "the app states an answer in text", "add an 'Our answer' section")
    ok(re.search(r"#+ What this data cannot show", texts()) is not None, "9", "the app states what the data cannot show")

    allowed = {c.lower() for c in SERIES[:3] + [CONTEXT]}
    n_charts, footers, errors, axis_issues, label_issues, colour_issues = 0, [], [], [], [], []
    widgets = []
    for page in PAGES:
        at.switch_page(page).run()
        if at.exception:
            errors.append(f"{page}: {at.exception[0].value[:120]}")
            continue
        footers.append(any("Data last refreshed" in c.value for c in at.caption))
        specs = chart_specs(at)
        n_charts += len(specs)
        for k, spec in enumerate(specs, start=1):
            where = f"{Path(page).stem} chart {k}"
            lay, traces = spec.get("layout", {}), spec.get("data", [])
            xt = (lay.get("xaxis", {}).get("title") or {}).get("text")
            yt = (lay.get("yaxis", {}).get("title") or {}).get("text")
            if not xt or not yt:
                axis_issues.append(f"{where}: axis title missing")
            shown = [t for t in traces if t.get("showlegend", True) is not False and t.get("hoverinfo") != "skip"]
            if len(shown) > 1 and not ((lay.get("legend") or {}).get("title") or {}).get("text"):
                axis_issues.append(f"{where}: legend title missing")
            for t in shown:
                has_text = "text" in str(t.get("mode", "")) or t.get("type") == "bar" and t.get("text") is not None
                if not has_text and not t.get("texttemplate"):
                    label_issues.append(f"{where}: '{t.get('name')}' has no value labels")
                for colour in re.findall(r"#[0-9a-fA-F]{6}", json.dumps(t.get("marker", {})) + json.dumps(t.get("line", {}))):
                    if colour.lower() not in allowed and colour.lower() not in {"#fcfcfb", "#ffffff"}:
                        colour_issues.append(f"{where}: {colour}")
        for kind in ["multiselect", "selectbox", "radio", "segmented_control", "pills", "slider", "select_slider",
                     "checkbox", "toggle"]:
            for w in getattr(at, kind):
                widgets.append((page, kind, w.key))
    ok(not errors, "27", "every page runs without an error", "; ".join(errors))
    ok(n_charts >= 4, "13", "the app has at least four charts", f"{n_charts} charts", f"{n_charts} charts")
    ok(all(footers) and len(footers) == len(PAGES), "24", "sources and last data refresh are on every page")
    ok(not axis_issues, "16", "every axis and legend is labelled", "; ".join(axis_issues[:6]))
    record("PASS" if not label_issues else "WARN", "17", "every chart series carries visible value labels",
           "; ".join(label_issues[:6]))
    ok(not colour_issues, "18", "charts only use the colour-blind-checked palette in utils/theme.py",
       "; ".join(sorted(set(colour_issues))[:6]))

    # Interactions: each widget must change a chart, a metric or the text, quickly and without an error.
    working, slow, empty_ok, empty_bad = [], [], [], []
    for page, kind, key in widgets:
        if not key:
            continue
        at.switch_page(page).run()
        before = json.dumps(chart_specs(at)) + texts()
        w = getattr(at, kind)(key=key)
        if kind in {"multiselect"}:
            new = w.options[:1] if list(w.value) != w.options[:1] else w.options[1:2]
        elif kind in {"checkbox", "toggle"}:
            new = not w.value
        elif kind in {"slider", "select_slider"}:
            continue
        else:
            new = next((o for o in w.options if o != w.value), None)
        t0 = time.time()
        w.set_value(new).run()
        took = time.time() - t0
        if not at.exception and (json.dumps(chart_specs(at)) + texts()) != before:
            working.append(f"{Path(page).stem}:{key}")
            if took > 1.5:
                slow.append(f"{key} {took:.1f}s")
        if kind == "multiselect":
            at.switch_page(page).run()
            getattr(at, kind)(key=key).set_value([]).run()
            msg = list(at.info) + list(at.warning)
            (empty_ok if not at.exception and msg else empty_bad).append(f"{Path(page).stem}:{key}")
    ok(len(working) >= 2 and not slow, "21", "at least two interactions change what is shown, within about a second",
       f"working: {working}; slow: {slow}", ", ".join(working))
    ok(bool(empty_ok) and not empty_bad, "22", "an empty filter shows a message, not an error or a blank",
       f"no message for: {empty_bad}" if empty_bad else "no multiselect filter found", ", ".join(empty_ok))


def manual_items() -> None:
    for no, text in [
        ("3", "the question is arguable: the same data could support a different answer"),
        ("6", "each user story can be walked through in the app"),
        ("7", "every displayed number is in, or computed from, the data package (no typed-in numbers)"),
        ("10", "units, baselines and time coverage stated wherever numbers are compared"),
        ("11", "on-screen claims stay within what the data shows"),
        ("12", "every chart has a title or caption stating what it shows"),
        ("14", "charts span at least three Visual Vocabulary families"),
        ("15", "each chart's form matches its task"),
        ("19", "deployed URL loads in under five seconds (time it in a private window)"),
        ("20", "the app opens on something true about the whole dataset"),
        ("23", "layout works at 1366x768 with vertical scrolling only"),
        ("27", "the submitted tag resolves and the deployed app runs from it"),
    ]:
        record("MANUAL", no, text)


def main() -> int:
    pending = set()
    if "--pending" in sys.argv:
        pending = set(sys.argv[sys.argv.index("--pending") + 1].split(","))
    for step in (check_data_package, check_docs, check_app):
        try:
            step()
        except Exception as exc:  # report and keep going so one failure does not hide the rest
            record("FAIL", "-", f"{step.__name__} crashed", f"{type(exc).__name__}: {exc}"[:300])
    manual_items()
    for i, (status, no, check, detail) in enumerate(RESULTS):
        if status == "FAIL" and no in pending:
            RESULTS[i] = ("WARN", no, check, f"(pending) {detail}")
    order = {"FAIL": 0, "WARN": 1, "PASS": 2, "MANUAL": 3}
    width = max(len(r[2]) for r in RESULTS)
    for status, no, check, detail in sorted(RESULTS, key=lambda r: (order[r[0]], int(r[1]) if r[1].isdigit() else 0)):
        print(f"{status:6} #{no:>2}  {check:<{width}}  {detail}")
    counts = {s: sum(r[0] == s for r in RESULTS) for s in order}
    print("\n" + "  ".join(f"{k}: {v}" for k, v in counts.items()))
    return 1 if counts["FAIL"] else 0


if __name__ == "__main__":
    sys.exit(main())
