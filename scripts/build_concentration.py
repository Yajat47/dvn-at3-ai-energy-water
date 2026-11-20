"""Build the compute concentration processed datasets from Epoch AI notable models.

Owner: Sai Akarsh Viragani.
Reads data/samples/epoch_notable_ai_models.csv and produces:
- data/processed/compute_concentration_orgs.csv: compute breakdown by leading organizations and geographic groups since 2020
- data/processed/compute_concentration_countries.csv: compute breakdown by primary country since 2020
"""

from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "data" / "samples" / "epoch_notable_ai_models.csv"
OUT = ROOT / "data" / "processed"


def build_concentration() -> tuple[pd.DataFrame, pd.DataFrame]:
    df = pd.read_csv(SRC)
    df["year"] = pd.to_datetime(df["Publication date"], errors="coerce").dt.year
    valid = df[df["Training compute (FLOP)"].notna() & (df["Training compute (FLOP)"] > 0) & (df["year"] >= 2020)].copy()
    valid["year"] = valid["year"].astype(int)

    # Normalize primary organization and country
    valid["primary_org"] = valid["Organization"].fillna("Other").apply(lambda x: str(x).split(",")[0].strip())
    valid["primary_org"] = valid["primary_org"].replace({"Google": "Google DeepMind"})
    valid["primary_country"] = valid["Country (of organization)"].fillna("Unknown").apply(lambda x: str(x).split(",")[0].strip())

    tot_flop = valid["Training compute (FLOP)"].sum()

    # Top named individual organizations
    top_orgs = ["OpenAI", "xAI", "Meta AI", "Google DeepMind", "Anthropic", "Cursor", "Alibaba"]

    org_rows = []
    for org in top_orgs:
        p = valid[valid["primary_org"] == org]
        top_m = p.sort_values("Training compute (FLOP)", ascending=False).iloc[0]
        c_flop = p["Training compute (FLOP)"].sum()
        country = "China" if org == "Alibaba" else "United States"
        org_rows.append({
            "organization": org,
            "country": country,
            "models_count": int(len(p)),
            "total_compute_zettaflops": round(float(c_flop / 1e21), 2),
            "total_compute_flop": float(c_flop),
            "share_pct": round(float(c_flop / tot_flop * 100), 2),
            "largest_model": str(top_m["Model"]),
            "latest_year": int(p["year"].max()),
        })

    # Group remaining US developers (e.g. Nvidia, Microsoft, Amazon, US universities)
    p_us_other = valid[(~valid["primary_org"].isin(top_orgs)) & (valid["primary_country"].str.contains("United States"))]
    top_m_us = p_us_other.sort_values("Training compute (FLOP)", ascending=False).iloc[0]
    us_other_flop = p_us_other["Training compute (FLOP)"].sum()
    org_rows.append({
        "organization": "Other US organizations",
        "country": "United States",
        "models_count": int(len(p_us_other)),
        "total_compute_zettaflops": round(float(us_other_flop / 1e21), 2),
        "total_compute_flop": float(us_other_flop),
        "share_pct": round(float(us_other_flop / tot_flop * 100), 2),
        "largest_model": str(top_m_us["Model"]),
        "latest_year": int(p_us_other["year"].max()),
    })

    # Group remaining Chinese developers (e.g. ByteDance, DeepSeek, Moonshot, Baidu, Tsinghua)
    p_cn_other = valid[(~valid["primary_org"].isin(top_orgs)) & (valid["primary_country"] == "China")]
    top_m_cn = p_cn_other.sort_values("Training compute (FLOP)", ascending=False).iloc[0]
    cn_other_flop = p_cn_other["Training compute (FLOP)"].sum()
    org_rows.append({
        "organization": "Other Chinese organizations",
        "country": "China",
        "models_count": int(len(p_cn_other)),
        "total_compute_zettaflops": round(float(cn_other_flop / 1e21), 2),
        "total_compute_flop": float(cn_other_flop),
        "share_pct": round(float(cn_other_flop / tot_flop * 100), 2),
        "largest_model": str(top_m_cn["Model"]),
        "latest_year": int(p_cn_other["year"].max()),
    })

    # Group all remaining international organizations outside the US and China
    p_row = valid[(~valid["primary_org"].isin(top_orgs)) & (~valid["primary_country"].str.contains("United States|China"))]
    top_m_row = p_row.sort_values("Training compute (FLOP)", ascending=False).iloc[0]
    row_flop = p_row["Training compute (FLOP)"].sum()
    org_rows.append({
        "organization": "Rest of world organizations",
        "country": "Rest of world",
        "models_count": int(len(p_row)),
        "total_compute_zettaflops": round(float(row_flop / 1e21), 2),
        "total_compute_flop": float(row_flop),
        "share_pct": round(float(row_flop / tot_flop * 100), 2),
        "largest_model": str(top_m_row["Model"]),
        "latest_year": int(p_row["year"].max()),
    })

    org_df = pd.DataFrame(org_rows)

    # Country breakdown (exact same sums)
    top_countries = ["United States of America", "China"]
    cntry_rows = []
    for c in top_countries:
        p = valid[valid["primary_country"] == c]
        top_m = p.sort_values("Training compute (FLOP)", ascending=False).iloc[0]
        c_flop = p["Training compute (FLOP)"].sum()
        cntry_rows.append({
            "country": "United States" if "United States" in c else c,
            "models_count": int(len(p)),
            "total_compute_zettaflops": round(float(c_flop / 1e21), 2),
            "total_compute_flop": float(c_flop),
            "share_pct": round(float(c_flop / tot_flop * 100), 2),
            "top_organization": str(top_m["Organization"]).split(",")[0].strip(),
            "latest_year": int(p["year"].max()),
        })

    rest_c = valid[~valid["primary_country"].isin(top_countries)]
    top_m_rc = rest_c.sort_values("Training compute (FLOP)", ascending=False).iloc[0]
    rc_flop = rest_c["Training compute (FLOP)"].sum()
    cntry_rows.append({
        "country": "Rest of world",
        "models_count": int(len(rest_c)),
        "total_compute_zettaflops": round(float(rc_flop / 1e21), 2),
        "total_compute_flop": float(rc_flop),
        "share_pct": round(float(rc_flop / tot_flop * 100), 2),
        "top_organization": str(top_m_rc["Organization"]).split(",")[0].strip(),
        "latest_year": int(rest_c["year"].max()),
    })
    cntry_df = pd.DataFrame(cntry_rows)

    return org_df, cntry_df


def main() -> None:
    org_df, cntry_df = build_concentration()
    OUT.mkdir(parents=True, exist_ok=True)
    org_path = OUT / "compute_concentration_orgs.csv"
    cntry_path = OUT / "compute_concentration_countries.csv"
    org_df.to_csv(org_path, index=False)
    cntry_df.to_csv(cntry_path, index=False)
    print(f"wrote {len(org_df)} rows to {org_path.relative_to(ROOT)}")
    print(f"wrote {len(cntry_df)} rows to {cntry_path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
