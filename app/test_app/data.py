from pathlib import Path

import pandas as pd
import streamlit as st

from config import NUMERIC_COLUMNS

@st.cache_data
def load_data(path: Path) -> pd.DataFrame:
    """
    Load the country panel data and convert selected columns to numeric.
    """
    df = pd.read_parquet(path)

    for col in NUMERIC_COLUMNS:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    return df


def get_country_options(df: pd.DataFrame) -> pd.DataFrame:
    """
    Create a country option table from iso3 and area.
    """
    required_cols = ["iso3", "area"]
    missing_cols = [col for col in required_cols if col not in df.columns]

    if missing_cols:
        raise ValueError(f"Missing required columns: {missing_cols}")

    options = (
        df.loc[:, ["iso3", "area"]]
        .dropna()
        .drop_duplicates()
        .sort_values(["area", "iso3"])
        .reset_index(drop=True)
    )

    return options


def get_year_range(df: pd.DataFrame) -> tuple[int, int]:
    """
    Return the minimum and maximum year in the dataset.
    """
    if "year" not in df.columns:
        raise ValueError("The input data must contain a 'year' column.")

    year_series = df["year"].dropna()

    if year_series.empty:
        raise ValueError("No valid year data found.")

    min_year = int(year_series.min())
    max_year = int(year_series.max())

    return min_year, max_year


def get_default_country_index(country_options: pd.DataFrame, default_iso3: str) -> int:
    """
    Return the default index for the country selectbox.
    """
    if default_iso3 in country_options["iso3"].values:
        return int(country_options.index[country_options["iso3"] == default_iso3][0])

    return 0

def filter_country_data(df, iso3_list, year_range):
    min_year, max_year = year_range

    return df[
        (df["iso3"].isin(iso3_list)) &
        (df["year"] >= min_year) &
        (df["year"] <= max_year)
    ].copy()