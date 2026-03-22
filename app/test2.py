from pathlib import Path

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

# =====================================
# Setting up the test environment
# =====================================
BASE_DIR = Path(__file__).resolve().parents[1]
DATA_PATH = BASE_DIR / "data" / "raw" / "country_panel.csv"

# Example dataframe
data_example = {
    "country": ["Country A", "Country A", "Country B", "Country B", "Country C", "Country C"],
    "year": [2000, 2001, 2000, 2001, 2000, 2001],
    "crop_land_ha": [1000, 1500, 1200, 1100, 1300, 1400],
    "share_irrigated_percent": [20, 30, 25, 22, 28, 32]
}
df = pd.DataFrame(data_example)
country_options = df[["country"]].drop_duplicates().reset_index(drop=True)

# =====================================
# Title
# =====================================
st.title("Macro Statistics Dashboard")

# =====================================
# Sidebar filters
# =====================================
with st.sidebar:
    st.header("Filters")
    multiple_countries = st.multiselect("Multiple country selection",
                                        options=country_options["country"],
                                        default="Country A")
    st.write("You selected in page1:", multiple_countries)

# Data sources
col1, col2 = st.columns(2)

with col1:
    st.link_button(label="FAOSTAT", 
                   url="https://www.fao.org/faostat/en/#home",
                   icon="➡",
                   icon_position="right")
    st.markdown("source: [FAOSTAT](https://www.fao.org/faostat/en/#home)")

with col2:
    st.link_button(label="WDI", 
                   url="https://databank.worldbank.org/source/world-development-indicators",
                   icon="➡",
                   icon_position="right")

# First sectio
st.header("Results")



st.subheader("Sample Data")
st.dataframe(df,
             column_config= {
                 "country": "Country",
                 "year": "Year",
                 "crop_land_ha": "Crop Land (1000 ha)",
                 "share_irrigated_percent": "Irrigated Share (%)"
             })

note = "Note: This is a sample dataset. The actual dataset will be loaded from the specified path and visualized accordingly."
st.markdown(note)

# Example selectbox for country selection

country = st.selectbox("Single country selection",
                       options=country_options["country"],
                       index=None,
                       placeholder="Select a country")

st.write(f"You selected: {country}")

# Example columns
col1, col2 = st.columns(2)

land_mean = df["crop_land_ha"].mean()
irrigation_mean = df["share_irrigated_percent"].mean()

with col1:
    st.metric("Average Crop Land (1000 ha)", f"{land_mean:.2f}", border=True)
with col2:
    color = st.color_picker("Pick A Color", "#00f900")
    
    st.metric("Average Irrigated Share (%)", 
    f"{irrigation_mean:.2f}",
    chart_data=df["share_irrigated_percent"],
    chart_type="line")