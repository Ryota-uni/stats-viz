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
st.title("Time Series Data Table")

years = st.session_state.get("year_slider")
coutries = st.session_state.get("country_multiselect")

crop_selection = df[
    (df["country"].isin(coutries)) & (df["year"].between(years[0], years[1]))
    ][["year", "crop_land_ha"]]

st.markdown("### Crop land (1000 ha)")
st.dataframe(crop_selection)