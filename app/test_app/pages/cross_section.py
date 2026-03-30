import plotly.express as px
import streamlit as st

from config import DATA_PATH, GROUP_INFO_PATH, CROSS_SECTION_SCATTERS
from data import (
    load_data,
    load_country_group_info,
    add_country_groups,
    smooth_and_downsample_cross_section,
)
from components import render_data_sources, render_scatter_panel

#-----------------------------
# Page setup
#-----------------------------
st.set_page_config(
    page_title="Cross Section",
    layout="wide",
)

st.title("Macro Statistics Viewer: Cross Section")
render_data_sources()

#-----------------------------
# Load data
#-----------------------------
df = load_data(DATA_PATH)
group_df = load_country_group_info(GROUP_INFO_PATH)
df = add_country_groups(df, group_df)

# -----------------------------
# Prepare columns for smoothing
# -----------------------------
all_value_cols = sorted(
    {
        spec["x"]
        for spec in CROSS_SECTION_SCATTERS
    }.union(
        {
            spec["y"]
            for spec in CROSS_SECTION_SCATTERS
        }
    ).union(
        {
            spec["size"]
            for spec in CROSS_SECTION_SCATTERS
            if spec["size"] is not None
        }
    )
)

group_cols = ["iso3", "area", "sub_region"]

df_plot = smooth_and_downsample_cross_section(
    df=df,
    group_cols=group_cols,
    value_cols=all_value_cols,
    year_col="year",
    start_year=1960,
    end_year=2020,
    step=5,
    window_radius=2,
)

if df_plot.empty:
    st.warning("No data available for cross-section plots.")
    st.stop()

# -----------------------------
# Render scatter panels
# -----------------------------
for row_start in range(0, len(CROSS_SECTION_SCATTERS), 2):
    cols = st.columns(2, border=True)
    row_specs = CROSS_SECTION_SCATTERS[row_start:row_start + 2]

    for col, spec in zip(cols, row_specs):
        required_cols = ["iso3", "area", "year", "sub_region", spec["x"], spec["y"]]

        if spec["size"] is not None:
            required_cols.append(spec["size"])

        required_cols = list(dict.fromkeys(required_cols))
        df_scatter = df_plot[required_cols].dropna().copy()

        with col:
            if df_scatter.empty:
                st.info(f"No data available for {spec['title']}.")
            else:
                render_scatter_panel(
                    df=df_scatter,
                    title=spec["title"],
                    x=spec["x"],
                    y=spec["y"],
                    x_label=spec["x_label"],
                    y_label=spec["y_label"],
                    x_format=spec["x_format"],
                    y_format=spec["y_format"],
                    size=spec["size"],
                    key_prefix=spec["key_prefix"],
                )