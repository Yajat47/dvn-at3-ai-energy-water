"""Build data/processed/water_google.csv from the manual Google 2026 Environmental Report numbers.

Transform: keep the 2025 rows, add a plain-English label, write one row per metric.
The Dalles share of Google's total = 0.469 / 10.9 x 100 (computed on the page, not typed).
"""
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "data/samples/manual/google_2026_water.csv"
OUT = ROOT / "data/processed/water_google.csv"

LABELS = {
    "water_consumption_total": "Google total consumption (data centres and offices)",
    "water_consumption_growth": "Growth in consumption, 2024 to 2025",
    "water_consumption_the_dalles": "The Dalles, Oregon site consumption",
    "water_replenished_total": "Water replenished by stewardship projects",
    "water_replenished_share_of_freshwater": "Replenished, as reported, share of freshwater consumption",
}


def build() -> pd.DataFrame:
    raw = pd.read_csv(RAW)
    missing = set(LABELS) - set(raw["metric"])
    if missing:
        raise SystemExit(f"Missing metrics in {RAW.name}: {sorted(missing)}")
    out = raw.assign(label=raw["metric"].map(LABELS))[["metric", "label", "year", "value", "unit"]]
    if out["value"].isna().any():
        raise SystemExit("Empty value in the manual file.")
    OUT.parent.mkdir(parents=True, exist_ok=True)
    out.to_csv(OUT, index=False)
    return out


if __name__ == "__main__":
    print(build())
