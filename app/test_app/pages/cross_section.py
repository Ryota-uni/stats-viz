import plotly.express as px
import streamlit as st

from config import DATA_PATH, GROUP_INFO_PATH
from data import (
    load_data,
    load_country_group_info,
    add_country_groups,
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

df_plot = df[
    ["iso3", "area", "year", "crop_land_ha", "share_irrigated_percent", "fertilizer_consumption_kg_per_ha", "sub_region"]
].dropna().copy()


col1, col2 = st.columns(2, border=True)

with col1:
    render_scatter_panel(
        df=df_plot,
        title="Fertilizer Consumption vs. Share of Irrigated Area",
        x="fertilizer_consumption_kg_per_ha",
        y="share_irrigated_percent",
        x_label="Fertilizer Consumption (kg/ha)",
        y_label="Share of Irrigated Area (%)",
        x_format=".2f",
        y_format=".2f",
        size="crop_land_ha",
        key_prefix="scatter1",
    )

with col2:
    render_scatter_panel(
        df=df_plot,
        title="Fertilizer Consumption vs. Crop Land",
        x="fertilizer_consumption_kg_per_ha",
        y="crop_land_ha",
        x_label="Fertilizer Consumption (kg/ha)",
        y_label="Crop Land (ha)",
        x_format=".2f",
        y_format=".2f",
        size=None,
        key_prefix="scatter2",
    )