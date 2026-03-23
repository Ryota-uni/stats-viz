import plotly.express as px
import streamlit as st

from config import DATA_PATH, TIME_SERIES_INDICATORS
from data import load_data, filter_country_data, prepare_timeseries_data
from components import render_data_sources, render_timeseries_section

#-----------------------------
# Page setup
#-----------------------------
st.set_page_config(
    page_title="Time Series",
    page_icon="📈",
    layout="wide",
)

st.title("Macro Statistics Viewer: Time Series")
render_data_sources()

#-----------------------------
# Load data
#-----------------------------
df = load_data(DATA_PATH)

selected_iso3_multi = st.session_state.get("country_multi")
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

df_selected = filter_country_data(
    df=df,
    iso3_list=selected_iso3_multi,
    year_range=selected_year_range,
)

#-----------------------------
# Render time series sections
#-----------------------------
variables = [
    "gdp_per_capita_2015",
    "population_total",
    "crop_land_ha",
    "share_irrigated_percent",
    "agri_labor",
    "fertilizer_consumption_kg_per_ha",
]

for row_start in range(0, len(variables), 2):
    cols = st.columns(2, border=True)
    row_variables = variables[row_start:row_start + 2]

    for col, variable in zip(cols, row_variables):
        indicator_info = TIME_SERIES_INDICATORS[variable]
        df_plot, growth_col = prepare_timeseries_data(df_selected, variable)

        if df_plot.empty:
            continue

        with col:
            render_timeseries_section(
                df_plot=df_plot,
                variable=variable,
                growth_col=growth_col,
                indicator_info=indicator_info,
            )