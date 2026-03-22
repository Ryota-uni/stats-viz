import streamlit as st

from config import DATA_PATH, DEFAULT_ISO3
from data import (
    get_country_options,
    get_default_country_index,
    get_year_range,
    load_data,
)

from components import render_data_sources

#-----------------------------
# Page setup
#-----------------------------
st.set_page_config(
    page_title="Debug Page",
    page_icon="📊",
)

#-----------------------------
# Page top
#-----------------------------
st.title("Macro Statistics Viewer: Debug Page")

render_data_sources()

# -----------------------------
# Load data
# -----------------------------
df = load_data(DATA_PATH)

# -----------------------------
# Display current selections and data check - for debugging
# -----------------------------
selected_iso3_single = st.session_state.get("country_single")
selected_iso3_multi = st.session_state.get("country_multi")
selected_year_range = st.session_state.get("year_slider")


# Check current selections
with st.container():
    st.subheader("Check Current Selections")
    st.write("Selected  country:", selected_iso3_single)
    st.write("Selected multi country:", selected_iso3_multi)
    st.write("Selected year range:", selected_year_range)
    
# Check data loading (Zambia)
with st.container():
    st.subheader("Check Data Loading")
    st.write("Dataframe shape:", df.shape)
    st.write("Dataframe columns:", df.columns.tolist())
    st.dataframe(df.loc[df["iso3"] == DEFAULT_ISO3])
