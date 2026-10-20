"""Offline mode: regenerate every processed file from the source samples, then render the data dictionary.

Run from the repo root:  python scripts/build_all.py

Runs every scripts/build_*.py (each reads data/samples/ and writes data/processed/), then writes
data/DATA_DICTIONARY.md from data/data_dictionary.yml. Never touches data/samples/.
"""

import subprocess
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]


def run_builds() -> None:
    for script in sorted((ROOT / "scripts").glob("build_*.py")):
        if script.name == "build_all.py":
            continue
        print(f"--> {script.relative_to(ROOT)}")
        subprocess.run([sys.executable, str(script)], cwd=ROOT, check=True, timeout=120)


def cell(value) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ")


def render_dictionary_text() -> str:
    d = yaml.safe_load((ROOT / "data" / "data_dictionary.yml").read_text(encoding="utf-8"))
    sources = {s["id"]: s for s in d["sources"]}
    out = [
        "# Data dictionary",
        "",
        "Generated from `data/data_dictionary.yml` by `scripts/build_all.py`. Edit the YAML, not this file.",
        "",
        "## Sources",
        "",
        "| ID | Title | Publisher | URL | Licence | Retrieved |",
        "|---|---|---|---|---|---|",
    ]
    for s in d["sources"]:
        out.append(f"| `{s['id']}` | {cell(s['title'])} | {cell(s['publisher'])} | {s['url']} | {cell(s['licence'])} | {s['retrieved']} |")
    for role, heading in [("sample", "Source samples"), ("processed", "Processed files the app reads")]:
        out += ["", f"## {heading}"]
        for ds in [x for x in d["datasets"] if x["role"] == role]:
            src = [sources[i] for i in ds["source_ids"]]
            out += [
                "",
                f"### `{ds['path']}`",
                "",
                cell(ds["description"]),
                "",
                f"- **Dataset ID:** `{ds['id']}` (owner: {ds.get('owner', 'n/a')})",
                f"- **Source:** " + "; ".join(f"{s['publisher']}, *{s['title']}*" for s in src),
                f"- **URL:** " + "; ".join(s["url"] for s in src),
                f"- **Licence:** " + "; ".join(s["licence"] for s in src),
                f"- **Primary key:** " + ", ".join(f"`{k}`" for k in ds["primary_key"]),
                f"- **Time coverage:** {ds['time_coverage']}",
                f"- **Latest observation:** {ds['latest_observation']}",
            ]
            if ds.get("metadata_file"):
                out.append(f"- **Source metadata:** `{ds['metadata_file']}`")
            t = ds["transform"]
            if isinstance(t, str):
                out.append(f"- **Transform:** {t}")
            else:
                out.append(f"- **Transform:** `{t['script']}` from " + ", ".join(f"`{i}`" for i in t["inputs"]))
                out += [f"  {n}. {step}" for n, step in enumerate(t["steps"], start=1)]
            out += ["", "| Column | Type | Unit | Description |", "|---|---|---|---|"]
            for name, spec in ds["columns"].items():
                out.append(f"| `{cell(name)}` | {spec['type']} | {cell(spec['unit'])} | {cell(spec['description'])} |")
    return "\n".join(out) + "\n"


def render_dictionary() -> None:
    (ROOT / "data" / "DATA_DICTIONARY.md").write_text(render_dictionary_text(), encoding="utf-8")
    print("--> wrote data/DATA_DICTIONARY.md")


if __name__ == "__main__":
    run_builds()
    render_dictionary()
