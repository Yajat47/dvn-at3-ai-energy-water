"""Loading helpers. Pages read processed files only; scripts/ turns raw files into processed ones."""

from pathlib import Path

import pandas as pd
import streamlit as st

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"
PROCESSED = ROOT / "data" / "processed"


@st.cache_data
def processed(name: str) -> pd.DataFrame:
    """Read data/processed/<name>.csv."""
    return pd.read_csv(PROCESSED / f"{name}.csv")


@st.cache_data
def raw(relative_path: str) -> pd.DataFrame:
    """Read a CSV under data/raw/ (for showing source rows in a trace)."""
    return pd.read_csv(RAW / relative_path)


@st.cache_data
def sources() -> pd.DataFrame:
    """The source registry, one row per source."""
    return pd.read_csv(ROOT / "sources.csv")
