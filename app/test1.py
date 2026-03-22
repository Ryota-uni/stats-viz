import pandas as pd
from pathlib import Path
import streamlit as st

# =====================================
# Setting up the test environment
# =====================================
data_example = {
    "country": ["Country A", "Country A", "Country B", "Country B", "Country C", "Country C"],
    "year": [2000, 2001, 2000, 2001, 2000, 2001],
    "crop_land_ha": [1000, 1500, 1200, 1100, 1300, 1400],
    "share_irrigated_percent": [20, 30, 25, 22, 28, 32]
}
df = pd.DataFrame(data_example)
country_options = df[["country"]].drop_duplicates().reset_index(drop=True)

# =====================================
# Setting sidebar options
# =====================================
st.sidebar.header("Data Filters")

cast_countries = st.sidebar.multiselect(
    "Country selection",
    options=country_options["country"],
    default="Country A",
    key="country_multiselect"
    )

Years = st.sidebar.slider(
    "Year selection",
    min_value=int(df["year"].min()),
    max_value=int(df["year"].max()),
    value=(int(df["year"].min()), int(df["year"].max())),
    step=1,
    key="year_slider"
)

# =====================================
# Setting pages
# =====================================
pages = {
    "Cross Country Analysis": [
        st.Page("test_data_cross.py", title="Data Table"),
        st.Page("test2.py", title="FAO"),
    ],
    "Time Series Analysis": [
        st.Page("test_data_time.py", title="Data Table"),
    ],
}



pg = st.navigation(pages, position="sidebar")
pg.run()