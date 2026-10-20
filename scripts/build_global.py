"""Build the processed tables behind the Global scale page.

Run from the repo root:  python scripts/build_global.py

Inputs (data/samples/, source samples):
  owid_data_centers_share_electricity_demand.csv  IEA data-centre electricity as % of demand
  owid_ember_electricity_demand.csv               Ember total electricity demand, TWh
  manual/iea_2026_key_questions.csv               numbers transcribed from the IEA 2026 report

Outputs (data/processed/):
  global_dc_electricity.csv   data-centre TWh and share, World / US / China / Rest of world
  global_growth_index.csv     data-centre TWh vs all electricity demand, indexed to 2020 = 100
  global_comparisons.csv      2025 data-centre TWh next to whole countries' electricity demand

Method: OWID computes the share as IEA data-centre TWh / Ember demand TWh, so
multiplying the share back by Ember demand recovers the IEA TWh figure.
"""

from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
SAMPLES = ROOT / "data" / "samples"
OUT = ROOT / "data" / "processed"

ENTITIES = ["World", "United States", "China"]
COMPARE_WITH = ["Australia", "United Kingdom", "France", "Germany"]


def load_inputs() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    share = pd.read_csv(SAMPLES / "owid_data_centers_share_electricity_demand.csv").rename(
        columns={
            "Entity": "entity",
            "Year": "year",
            "Share of total electricity demand coming from data centers": "dc_share_pct",
        }
    )
    demand = pd.read_csv(SAMPLES / "owid_ember_electricity_demand.csv").rename(
        columns={"Entity": "entity", "Year": "year", "Electricity demand": "demand_twh"}
    )
    iea = pd.read_csv(SAMPLES / "manual" / "iea_2026_key_questions.csv")
    return share, demand, iea


def build_actuals(share: pd.DataFrame, demand: pd.DataFrame) -> pd.DataFrame:
    # Step 1: keep World, US and China; inner join keeps only years with both values.
    df = share[share["entity"].isin(ENTITIES)][["entity", "year", "dc_share_pct"]].merge(
        demand[demand["entity"].isin(ENTITIES)][["entity", "year", "demand_twh"]],
        on=["entity", "year"],
        how="inner",
    )
    # Step 2: data-centre TWh = share (%) / 100 x total demand (TWh).
    df["dc_twh"] = df["dc_share_pct"] / 100 * df["demand_twh"]

    # Step 3: Rest of world = World minus United States minus China.
    wide = df.pivot(index="year", columns="entity", values=["dc_twh", "demand_twh"])
    rest = pd.DataFrame(
        {
            "entity": "Rest of world",
            "year": wide.index,
            "demand_twh": (
                wide["demand_twh"]["World"] - wide["demand_twh"]["United States"] - wide["demand_twh"]["China"]
            ).values,
            "dc_twh": (wide["dc_twh"]["World"] - wide["dc_twh"]["United States"] - wide["dc_twh"]["China"]).values,
        }
    )
    rest["dc_share_pct"] = rest["dc_twh"] / rest["demand_twh"] * 100

    out = pd.concat([df, rest], ignore_index=True)
    out["kind"] = "actual"
    out["method"] = "IEA share (OWID) x Ember demand"
    out.loc[out["entity"] == "Rest of world", "method"] = "World minus United States minus China"
    return out


def add_projection(actuals: pd.DataFrame, iea: pd.DataFrame) -> pd.DataFrame:
    # Step 4: the IEA 2030 base-case point (TWh and share) from the transcribed report text.
    twh = iea.query("metric == 'data_centre_electricity' and year == 2030")["value"].item()
    pct = iea.query("metric == 'data_centre_share_of_world_electricity' and year == 2030")["value"].item()
    proj = pd.DataFrame(
        [
            {
                "entity": "World",
                "year": 2030,
                "dc_share_pct": pct,
                "demand_twh": float("nan"),
                "dc_twh": twh,
                "kind": "projection",
                "method": "IEA 2026 base case (report text)",
            }
        ]
    )
    return pd.concat([actuals, proj], ignore_index=True)


def build_index(actuals: pd.DataFrame) -> pd.DataFrame:
    # Step 5: index World data-centre TWh and World demand TWh to 2020 = 100.
    world = actuals[actuals["entity"] == "World"].sort_values("year")
    base = world[world["year"] == 2020].iloc[0]
    rows = []
    for _, r in world.iterrows():
        rows.append({"year": r["year"], "series": "Data-centre electricity", "twh": r["dc_twh"],
                     "index_2020": r["dc_twh"] / base["dc_twh"] * 100})
        rows.append({"year": r["year"], "series": "All electricity demand", "twh": r["demand_twh"],
                     "index_2020": r["demand_twh"] / base["demand_twh"] * 100})
    return pd.DataFrame(rows)


def build_comparisons(actuals: pd.DataFrame, demand: pd.DataFrame, year: int = 2025) -> pd.DataFrame:
    # Step 6: put the world data-centre total next to whole countries' demand in the same year.
    dc = actuals.query("entity == 'World' and year == @year")["dc_twh"].item()
    countries = demand[(demand["entity"].isin(COMPARE_WITH)) & (demand["year"] == year)][["entity", "demand_twh"]]
    countries = countries.assign(year=year, world_dc_twh=dc, ratio_dc_to_country=dc / countries["demand_twh"])
    return countries.sort_values("demand_twh")[["entity", "year", "demand_twh", "world_dc_twh", "ratio_dc_to_country"]]


def check(global_df: pd.DataFrame, iea: pd.DataFrame) -> None:
    """Fail loudly if our derived numbers drift from the IEA's published ones."""
    world = global_df[(global_df["entity"] == "World") & (global_df["kind"] == "actual")].set_index("year")
    iea_2025 = iea.query("metric == 'data_centre_electricity' and year == 2025")["value"].item()
    iea_growth = iea.query("metric == 'data_centre_electricity_growth' and year == 2025")["value"].item()

    derived_2025 = world.loc[2025, "dc_twh"]
    derived_growth = (world.loc[2025, "dc_twh"] / world.loc[2024, "dc_twh"] - 1) * 100

    assert abs(derived_2025 - iea_2025) < 2, f"2025 TWh {derived_2025:.1f} vs IEA {iea_2025}"
    assert abs(derived_growth - iea_growth) < 1.5, f"2025 growth {derived_growth:.1f}% vs IEA {iea_growth}%"
    print(f"check ok: World 2025 = {derived_2025:.1f} TWh (IEA {iea_2025}), "
          f"growth = {derived_growth:.1f}% (IEA {iea_growth}%)")


def main() -> None:
    share, demand, iea = load_inputs()
    actuals = build_actuals(share, demand)
    global_df = add_projection(actuals, iea).sort_values(["entity", "year"])
    index_df = build_index(actuals)
    comparisons_df = build_comparisons(actuals, demand)
    check(global_df, iea)

    OUT.mkdir(parents=True, exist_ok=True)
    cols = ["entity", "year", "kind", "dc_share_pct", "demand_twh", "dc_twh", "method"]
    global_df[cols].to_csv(OUT / "global_dc_electricity.csv", index=False, float_format="%.4f")
    index_df.to_csv(OUT / "global_growth_index.csv", index=False, float_format="%.4f")
    print(f"wrote {len(global_df)} rows to data/processed/global_dc_electricity.csv")
    comparisons_df.to_csv(OUT / "global_comparisons.csv", index=False, float_format="%.4f")
    print(f"wrote {len(index_df)} rows to data/processed/global_growth_index.csv")
    print(f"wrote {len(comparisons_df)} rows to data/processed/global_comparisons.csv")


if __name__ == "__main__":
    main()
