import plotly.express as px
import streamlit as st

from config import DATA_PATH, GROUP_INFO_PATH
from data import load_data, load_country_group_info, make_country_group_table
from components import render_data_sources

#-----------------------------
# Page setup
#-----------------------------
st.set_page_config(
    page_title="Top",
    layout="wide",
)

st.title("Macro Statistics Viewer")
render_data_sources()

#-----------------------------
# Load data
#-----------------------------
df = load_data(DATA_PATH)
group_df = load_country_group_info(GROUP_INFO_PATH)
country_group_table = make_country_group_table(df, group_df)

st.subheader("Country Group")
st.dataframe(country_group_table, use_container_width=True)