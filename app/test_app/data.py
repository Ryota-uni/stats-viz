from pathlib import Path

import pandas as pd
import streamlit as st
import json
from config import NUMERIC_COLUMNS, CROP_NUMERIC_COLUMNS

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

@st.cache_data
def load_crop_data(path: Path) -> pd.DataFrame:
    """
    Load the country panel data and convert selected columns to numeric.
    """
    df = pd.read_parquet(path)

    for col in CROP_NUMERIC_COLUMNS:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    return df

@st.cache_data
def load_country_group_info(path) -> pd.DataFrame:
    with open(path, "r", encoding="utf-8") as f:
        raw = json.load(f)

    group_info = raw["country_group_info"]

    rows = []
    for iso3, info in group_info.items():
        rows.append(
            {
                "iso3": iso3,
                "region": info.get("region"),
                "subregion": info.get("subregion"),
                "sub_region": info.get("sub_region"),
                "intermediate_region": info.get("intermediate_region"),
            }
        )

    return pd.DataFrame(rows)

def add_country_groups(df: pd.DataFrame, group_df: pd.DataFrame) -> pd.DataFrame:
    return df.merge(group_df, on="iso3", how="left")

def make_country_group_table(df: pd.DataFrame, group_df: pd.DataFrame) -> pd.DataFrame:
    area_df = (
        df[["iso3", "area"]]
        .dropna()
        .drop_duplicates()
        .sort_values(["area", "iso3"])
        .reset_index(drop=True)
    )

    table_df = (
        area_df.merge(group_df, on="iso3", how="left")
        .sort_values(["region", "sub_region", "area"])
        .reset_index(drop=True).reindex(columns=["region", "sub_region", "intermediate_region", "iso3", "area"])
    )

    return table_df

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

def get_crop_options(df: pd.DataFrame) -> pd.DataFrame:
    """
    Create a crop option table from iso3 and area.
    """
    required_cols = ["item_code", "crop"]
    missing_cols = [col for col in required_cols if col not in df.columns]

    if missing_cols:
        raise ValueError(f"Missing required columns: {missing_cols}")

    options = (
        df.loc[:, ["crop", "item_code"]]
        .dropna()
        .drop_duplicates()
        .sort_values(["crop", "item_code"])
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

def filter_country_crop_data(df, iso3_list, crop_list, year_range):
    min_year, max_year = year_range

    return df[
        (df["iso3"].isin(iso3_list)) &
        (df["crop"].isin(crop_list)) &
        (df["year"] >= min_year) &
        (df["year"] <= max_year)
    ].copy()

def prepare_timeseries_data(df, variable):
    df_plot = df[["iso3", "area", "year", variable]].dropna().copy()
    df_plot = df_plot.sort_values(["area", "year"]).copy()

    growth_col = f"{variable}_growth_percent"
    df_plot[growth_col] = (
        df_plot.groupby("area")[variable].pct_change() * 100
    )

    return df_plot, growth_col

def smooth_and_downsample_cross_section(
    df: pd.DataFrame,
    group_cols: list[str],
    value_cols: list[str],
    year_col: str = "year",
    start_year: int = 1960,
    end_year: int = 2020,
    step: int = 5,
    window_radius: int = 2,
) -> pd.DataFrame:
    """
    Create country-level smoothed cross-sectional data at anchor years.

    Example:
    1960 -> average of 1958, 1959, 1960, 1961, 1962
    1965 -> average of 1963, 1964, 1965, 1966, 1967

    Missing values are ignored in the mean calculation.
    """
    df = df.copy()

    # Make sure year is numeric
    df[year_col] = pd.to_numeric(df[year_col], errors="coerce")
    df = df.dropna(subset=[year_col]).copy()
    df[year_col] = df[year_col].astype(int)

    smoothed_list = []

    anchor_years = range(start_year, end_year + 1, step)

    for anchor_year in anchor_years:
        lower_year = anchor_year - window_radius
        upper_year = anchor_year + window_radius

        df_window = df[
            (df[year_col] >= lower_year) & (df[year_col] <= upper_year)
        ].copy()

        if df_window.empty:
            continue

        df_anchor = (
            df_window
            .groupby(group_cols, dropna=False)[value_cols]
            .mean()
            .reset_index()
        )

        df_anchor[year_col] = int(anchor_year)
        smoothed_list.append(df_anchor)

    if not smoothed_list:
        return pd.DataFrame(columns=group_cols + [year_col] + value_cols)

    df_out = pd.concat(smoothed_list, ignore_index=True)

    # Ensure year is integer and rows are ordered properly
    df_out[year_col] = pd.to_numeric(df_out[year_col], errors="coerce").astype(int)
    df_out = df_out.sort_values(group_cols + [year_col]).reset_index(drop=True)

    return df_out