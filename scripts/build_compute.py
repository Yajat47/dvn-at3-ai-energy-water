"""Build the processed tables behind the Compute vs efficiency page.

Run from the repo root:  python scripts/build_compute.py

Inputs (data/samples/, source samples):
    epoch_notable_ai_models.csv   Epoch AI Notable AI Models: training compute per model, FLOP
    epoch_ml_hardware.csv         Epoch AI Machine Learning Hardware: FP32 FLOP/s and TDP per chip

Outputs (data/processed/):
    compute_vs_efficiency.csv     best training compute and best hardware efficiency to date, by year,
                                  each indexed to BASE_YEAR = 1
    compute_growth_summary.csv    average yearly growth and doubling time for each series

Method: for each year, keep the record (largest model, most efficient chip) released up to and
including that year, so each line shows the frontier and never falls. Efficiency is FP32 FLOP/s
divided by TDP watts, because FP32 is reported for chips across the whole period.
"""

import math
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
SAMPLES = ROOT / "data" / "samples"
OUT = ROOT / "data" / "processed"

BASE_YEAR = 2012
COMPUTE_COL = "Training compute (FLOP)"
PERF_COL = "FP32 (single precision) performance (FLOP/s)"
TDP_COL = "TDP (W)"

COMPUTE_SERIES = "Training compute of the largest model"
EFFICIENCY_SERIES = "Efficiency of the best chip (FP32)"


def load_inputs() -> tuple[pd.DataFrame, pd.DataFrame]:
    models = pd.read_csv(SAMPLES / "epoch_notable_ai_models.csv")
    hardware = pd.read_csv(SAMPLES / "epoch_ml_hardware.csv")
    return models, hardware


def tidy_models(models: pd.DataFrame) -> pd.DataFrame:
    # Step 1: keep models with a publication date and a positive training-compute figure.
    df = pd.DataFrame({
        "name": models["Model"],
        "organization": models["Organization"],
        "date": pd.to_datetime(models["Publication date"], errors="coerce"),
        "value": pd.to_numeric(models[COMPUTE_COL], errors="coerce"),
    }).dropna(subset=["date", "value"])
    df = df[df["value"] > 0].copy()
    df["year"] = df["date"].dt.year
    return df


def tidy_hardware(hardware: pd.DataFrame) -> pd.DataFrame:
    # Step 2: efficiency = FP32 FLOP/s / TDP watts, for chips that report both.
    df = pd.DataFrame({
        "name": hardware["Hardware name"],
        "organization": hardware["Manufacturer"],
        "date": pd.to_datetime(hardware["Release date"], errors="coerce"),
        "perf_flops": pd.to_numeric(hardware[PERF_COL], errors="coerce"),
        "tdp_w": pd.to_numeric(hardware[TDP_COL], errors="coerce"),
    }).dropna(subset=["date", "perf_flops", "tdp_w"])
    df = df[(df["perf_flops"] > 0) & (df["tdp_w"] > 0)].copy()
    df["value"] = df["perf_flops"] / df["tdp_w"]
    df["year"] = df["date"].dt.year
    return df


def running_record(df: pd.DataFrame, series: str, unit: str, last_year: int) -> pd.DataFrame:
    # Step 3: for each year, the best value released up to and including that year.
    rows, best = [], None
    for year in range(int(df["year"].min()), last_year + 1):
        this_year = df[df["year"] == year]
        if not this_year.empty:
            top = this_year.loc[this_year["value"].idxmax()]
            if best is None or top["value"] > best["value"]:
                best = top
        if year >= BASE_YEAR and best is not None:
            rows.append({
                "year": year,
                "series": series,
                "value": best["value"],
                "unit": unit,
                "record_holder": best["name"],
                "record_organization": best["organization"],
                "record_year": int(best["year"]),
            })
    out = pd.DataFrame(rows)
    # Step 4: index to BASE_YEAR = 1 so both series share one log axis.
    base = out.loc[out["year"] == BASE_YEAR, "value"].item()
    out[f"index_{BASE_YEAR}"] = out["value"] / base
    return out


def build_summary(table: pd.DataFrame) -> pd.DataFrame:
    # Step 5: average growth per year and doubling time between BASE_YEAR and the last year.
    rows = []
    for series, part in table.groupby("series"):
        start = part.loc[part["year"] == BASE_YEAR, "value"].item()
        last = part.sort_values("year").iloc[-1]
        years = last["year"] - BASE_YEAR
        growth = (last["value"] / start) ** (1 / years)
        rows.append({
            "series": series,
            "start_year": BASE_YEAR,
            "end_year": int(last["year"]),
            "start_value": start,
            "end_value": last["value"],
            "total_multiple": last["value"] / start,
            "growth_per_year": growth,
            "doubling_time_months": 12 * math.log(2) / math.log(growth),
        })
    return pd.DataFrame(rows)


def check(table: pd.DataFrame, summary: pd.DataFrame) -> None:
    """Fail loudly if the table breaks the page's assumptions."""
    for series, part in table.groupby("series"):
        assert part["value"].is_monotonic_increasing, f"{series}: record should never fall"
        assert abs(part.loc[part["year"] == BASE_YEAR, f"index_{BASE_YEAR}"].item() - 1) < 1e-9
    assert (summary["growth_per_year"] > 1).all(), "both series should grow"
    for _, r in summary.iterrows():
        print(f"check ok: {r['series']}: x{r['total_multiple']:.3g} from {r['start_year']} to "
              f"{r['end_year']}, x{r['growth_per_year']:.2f} a year, doubling every "
              f"{r['doubling_time_months']:.1f} months")


def main() -> None:
    models, hardware = load_inputs()
    m, h = tidy_models(models), tidy_hardware(hardware)
    last_year = int(min(m["year"].max(), h["year"].max()))
    table = pd.concat([
        running_record(m, COMPUTE_SERIES, "FLOP", last_year),
        running_record(h, EFFICIENCY_SERIES, "FLOP/s per W", last_year),
    ], ignore_index=True)
    summary = build_summary(table)
    check(table, summary)

    OUT.mkdir(parents=True, exist_ok=True)
    table.to_csv(OUT / "compute_vs_efficiency.csv", index=False, float_format="%.6g")
    summary.to_csv(OUT / "compute_growth_summary.csv", index=False, float_format="%.6g")
    print(f"wrote {len(table)} rows to data/processed/compute_vs_efficiency.csv")
    print(f"wrote {len(summary)} rows to data/processed/compute_growth_summary.csv")


if __name__ == "__main__":
    main()