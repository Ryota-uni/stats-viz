import plotly.express as px
import streamlit as st

from config import CROP_DATA_PATH
from data import load_crop_data, filter_country_crop_data
from components import render_data_sources, render_crop_timeseries_section

#-----------------------------
# Page setup
#-----------------------------
st.set_page_config(
    page_title="Crop Statistics",
    layout="wide",
)

st.title("Macro Statistics Viewer: Crop")
render_data_sources()

#-----------------------------
# Load data
#-----------------------------
df = load_crop_data(CROP_DATA_PATH)

selected_iso3_multi = st.session_state.get("country_multi")
selected_crop_multi = st.session_state.get("crop_multi")
selected_year_range = st.session_state.get("year_slider")

if selected_iso3_multi is None:
    st.warning("Countries are not selected.")
    st.stop()

if len(selected_iso3_multi) == 0:
    st.warning("Please select at least one country.")
    st.stop()

if selected_year_range is None:
    st.warning("Year range is not selected.")
    st.stop()

if selected_crop_multi is None:
    st.warning("Crops are not selected.")
    st.stop()

if len(selected_crop_multi) == 0:
    st.warning("Please select at least one crop.")
    st.stop()

df_selected = filter_country_crop_data(
    df=df,
    iso3_list=selected_iso3_multi,
    crop_list=selected_crop_multi,
    year_range=selected_year_range,
)

st.dataframe(df_selected, use_container_width=True)

for crop in selected_crop_multi:
    df_crop = df_selected[df_selected["crop"] == crop].copy()

    if df_crop.empty:
        st.info(f"No data available for {crop}.")
        continue

    df_crop = df_crop.sort_values(["area", "year"]).copy()

    crop_info = {"label": crop}

    render_crop_timeseries_section(
        df_plot=df_crop,
        crop_name=crop_info,
    )