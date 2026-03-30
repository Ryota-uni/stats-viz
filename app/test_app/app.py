import streamlit as st

from config import DATA_PATH, CROP_DATA_PATH, DEFAULT_ISO3
from data import (
    get_country_options,
    get_crop_options,
    get_default_country_index,
    get_year_range,
    load_data,
    load_crop_data,
)

#-----------------------------
# Page setup
#-----------------------------
st.set_page_config(
    page_title="Macro Viewer",
)

#-----------------------------
# Load data
# -----------------------------
df = load_data(DATA_PATH)
df_crop = load_crop_data(CROP_DATA_PATH)

# -----------------------------
# Prepare sidebar options
# -----------------------------
country_options = get_country_options(df)
crop_options = get_crop_options(df_crop)
min_year, max_year = get_year_range(df)
default_index = get_default_country_index(country_options, DEFAULT_ISO3)

# -----------------------------
# Sidebar widgets
# -----------------------------
st.sidebar.header("Country and Year Selection")

selected_iso3_multi = st.sidebar.multiselect(
    "Multi Select Country",
    options=country_options["iso3"].tolist(),
    default=country_options["iso3"].iloc[default_index],
    format_func=lambda x: (
        country_options.loc[country_options["iso3"] == x, "area"].iloc[0] + f" ({x})"
    ),
    key="country_multi",
)

selected_crop_multi = st.sidebar.multiselect(
    "Multi Select Crop",
    options=crop_options["crop"].tolist(),
    default=None,
    format_func=lambda x: x,
    key="crop_multi",
)

selected_year_range = st.sidebar.slider(
    "Year range",
    min_value=min_year,
    max_value=max_year,
    value=(min_year, max_year),
    step=1,
    key="year_slider",
)

# -----------------------------
# Page navigation
# -----------------------------
pages = {
    "Home": [
        st.Page("pages/home.py", title="Home"),
    ],
    "Data Table": [
        st.Page("pages/data_table.py", title="Country Table"),
    ],
    "Graph": [
        st.Page("pages/cross_section.py", title="Cross Section"),
        st.Page("pages/timeseries.py", title="Time Series"),
        st.Page("pages/crop.py", title="Crop Statistics"),
    ],
    "Debug": [
        st.Page("pages/debug.py", title="Debug Page"),
    ],
}

pg = st.navigation(pages)
pg.run()