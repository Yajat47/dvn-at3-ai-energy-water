"""Loading helpers. Pages read processed files only; scripts/ turns source samples into processed files."""

from pathlib import Path

import pandas as pd
import streamlit as st
import yaml

ROOT = Path(__file__).resolve().parents[1]
SAMPLES = ROOT / "data" / "samples"
PROCESSED = ROOT / "data" / "processed"
DICTIONARY = ROOT / "data" / "data_dictionary.yml"


@st.cache_data
def processed(name: str) -> pd.DataFrame:
    """Read data/processed/<name>.csv."""
    return pd.read_csv(PROCESSED / f"{name}.csv")


@st.cache_data
def sample(relative_path: str) -> pd.DataFrame:
    """Read a CSV under data/samples/ (for showing source rows in a trace)."""
    return pd.read_csv(SAMPLES / relative_path)


@st.cache_data
def dictionary() -> dict:
    """The data dictionary: every source and dataset in the package."""
    return yaml.safe_load(DICTIONARY.read_text(encoding="utf-8"))


def sources() -> pd.DataFrame:
    """One row per source, from the data dictionary."""
    return pd.DataFrame(dictionary()["sources"])


def datasets() -> pd.DataFrame:
    """One row per dataset (samples and processed files), from the data dictionary."""
    return pd.DataFrame(dictionary()["datasets"])


def last_refresh() -> str:
    """Most recent retrieval date across all sources, for example '20 October 2026'."""
    latest = pd.to_datetime(sources()["retrieved"]).max()
    return f"{latest.day} {latest:%B %Y}"
