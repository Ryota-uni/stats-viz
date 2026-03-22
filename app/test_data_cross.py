from pathlib import Path

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

data_example = {
    "country": ["Country A", "Country A", "Country B", "Country B", "Country C", "Country C"],
    "year": [2000, 2001, 2000, 2001, 2000, 2001],
    "crop_land_ha": [1000, 1500, 1200, 1100, 1300, 1400],
    "share_irrigated_percent": [20, 30, 25, 22, 28, 32]
}
df = pd.DataFrame(data_example)

# =====================================
# Title
# =====================================
st.title("Cross Country Data Table")

years = st.session_state.get("year_slider")
years_max = int(years[1])

coutries = st.session_state.get("country_multiselect")

crop_selection_yearmax = df[
    (df["country"].isin(coutries)) & (df["year"] == years_max)
    ][["country", "crop_land_ha"]] 

st.markdown("### Crop land (1000 ha)")
st.dataframe(crop_selection_yearmax)