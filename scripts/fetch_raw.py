"""Download the raw source files used by the app into data/raw/.

Run from the repo root:  python scripts/fetch_raw.py

Raw files are never edited by hand. If a source updates, re-run this script,
update the `retrieved` date in sources.csv, then re-run the build scripts.
"""

from pathlib import Path
from urllib.request import Request, urlopen

RAW = Path(__file__).resolve().parents[1] / "data" / "raw"

# Our World in Data grapher exports: CSV (full data) + metadata JSON.
OWID_CHARTS = {
    # IEA data-centre electricity as a share of Ember electricity demand.
    "data-centers-share-electricity-demand": "owid_data_centers_share_electricity_demand",
    # Ember total electricity demand, TWh.
    "electricity-demand": "owid_ember_electricity_demand",
}


def download(url: str, dest: Path) -> None:
    req = Request(url, headers={"User-Agent": "dvn-at3-student-project/1.0"})
    with urlopen(req, timeout=60) as resp:
        dest.write_bytes(resp.read())
    print(f"saved {dest.relative_to(RAW.parents[1])} ({dest.stat().st_size:,} bytes)")


def main() -> None:
    RAW.mkdir(parents=True, exist_ok=True)
    for slug, name in OWID_CHARTS.items():
        base = f"https://ourworldindata.org/grapher/{slug}"
        download(f"{base}.csv?v=1&csvType=full&useColumnShortNames=false", RAW / f"{name}.csv")
        download(f"{base}.metadata.json?v=1&csvType=full&useColumnShortNames=false", RAW / f"{name}.metadata.json")


if __name__ == "__main__":
    main()
