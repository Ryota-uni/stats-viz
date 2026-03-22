import streamlit as st

from config import DATA_PATH
from data import load_data, filter_country_data
from components import render_data_sources

st.set_page_config(
    page_title="Data Table",
    layout="wide",
)

render_data_sources()

st.title("Macro Statistics Viewer: Data Table")

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

st.write("Selected countries:", selected_iso3_multi)
st.write("Selected year range:", selected_year_range)

st.dataframe(df_selected)