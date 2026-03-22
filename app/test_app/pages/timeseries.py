import plotly.express as px
import streamlit as st

from config import DATA_PATH
from data import load_data, filter_country_data
from components import render_data_sources

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

df_plot = df_selected[["iso3", "area", "year", "gdp_per_capita_2015"]].dropna().copy()
df_plot = df_plot.sort_values(["area", "year"]).copy()

if df_plot.empty:
    st.warning("No data available for the selected countries and years.")
    st.stop()

df_plot["gdp_growth_percent"] = (
    df_plot.groupby("area")["gdp_per_capita_2015"].pct_change() * 100
)

#-----------------------------
# Tool selection
#-----------------------------
option_map = {
    0: "Level",
    1: "Log Scale",
    2: "Growth Rate",
}
selection = st.segmented_control(
    "Tool",
    options=option_map.keys(),
    format_func=lambda option: option_map[option],
    selection_mode="single",
)

#-----------------------------
# Create line plot for GDP per capita
#-----------------------------
if selection == 2:
    fig = px.line(
        df_plot,
        x="year",
        y="gdp_growth_percent",
        color="area",
        markers=True,
        title="GDP per Capita Growth Rate (%)",
    )

    fig.update_yaxes(title="Growth rate (%)", linecolor="white", gridcolor="#E8EFE6")

    fig.update_traces(
        hovertemplate=
            "Country: %{fullData.name}<br>"
            "Year: %{x}<br>"
            "Growth rate: %{y:.2f}%<br>"
            "<extra></extra>"
    )

else:
    fig = px.line(
        df_plot,
        x="year",
        y="gdp_per_capita_2015",
        color="area",
        markers=True,
        title="GDP per Capita (2015 USD)",
    )

    if selection == 1:
        fig.update_yaxes(type="log", title="GDP per capita (log scale)", linecolor="white", gridcolor="#E8EFE6")
    else:
        fig.update_yaxes(type="linear", title="GDP per capita (2015 USD)", linecolor="white", gridcolor="#E8EFE6", gridwidth=1)

    fig.update_traces(
        hovertemplate=
            "Country: %{fullData.name}<br>"
            "Year: %{x}<br>"
            "GDP per capita: %{y:,.0f}<br>"
            "<extra></extra>"
    )

fig.update_xaxes(title="Year", linecolor="white")

st.plotly_chart(fig, use_container_width=True)