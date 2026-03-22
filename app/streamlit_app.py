from pathlib import Path

import pandas as pd
import plotly.graph_objects as go
import streamlit as st


# =====================================
# 1. Basic paths and app-level settings
# =====================================

BASE_DIR = Path(__file__).resolve().parents[1]
DATA_PATH = BASE_DIR / "data" / "raw" / "country_panel.csv"

DEFAULT_ISO3 = "ZMB"

CHART_SPECS = {
    "crop_land_ha": {
        "label": "Crop land (1000 ha)",
        "title": "Crop land area",
        "source": "FAOSTAT",
    },
    "share_irrigated_percent": {
        "label": "Irrigated share (%)",
        "title": "Share of irrigated agricultural land",
        "source": "FAOSTAT",
    },
    "agri_labor": {
        "label": "Agricultural labor",
        "title": "Agricultural labor",
        "source": "FAOSTAT",
    },
    "fertilizer_total_ton": {
        "label": "Fertilizer total (ton)",
        "title": "Fertilizer use",
        "source": "FAOSTAT",
    },
    "net_capital_2015": {
        "label": "Net capital (2015 USD)",
        "title": "Net capital stock",
        "source": "FAOSTAT",
    },
    "gdp_per_capita_2015": {
        "label": "GDP per capita (2015 USD)",
        "title": "GDP per capita",
        "source": "WDI",
    },
    "agri_gdp_share_percent": {
        "label": "Agricultural GDP share (%)",
        "title": "Agricultural GDP share",
        "source": "WDI",
    },
    "population_total": {
        "label": "Population",
        "title": "Total population",
        "source": "WDI",
    },
    "rural_population_share": {
        "label": "Rural population share (%)",
        "title": "Rural population share",
        "source": "WDI",
    },
    "agri_employment_share": {
        "label": "Agricultural employment share (%)",
        "title": "Agricultural employment share",
        "source": "WDI",
    },
}


# =====================================
# 2. Data loading and preprocessing
# =====================================

@st.cache_data
def load_data(path: Path) -> pd.DataFrame:
    """
    Load the country panel data and convert target columns to numeric.
    """
    df = pd.read_csv(path)

    numeric_columns = [
        "year",
        "crop_land_ha",
        "share_irrigated_percent",
        "agri_labor",
        "fertilizer_total_ton",
        "net_capital_2015",
        "gdp_per_capita_2015",
        "agri_gdp_share_percent",
        "population_total",
        "rural_population_share",
        "agri_employment_share",
    ]

    for col in numeric_columns:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    return df


def get_country_options(df: pd.DataFrame) -> pd.DataFrame:
    """
    Build a country option table from iso3 and area.
    """
    required_cols = ["iso3", "area"]
    available_cols = [c for c in required_cols if c in df.columns]

    if len(available_cols) < 2:
        raise ValueError("Both 'iso3' and 'area' columns are required in the input data.")

    options = (
        df.loc[:, ["iso3", "area"]]
        .dropna()
        .drop_duplicates()
        .sort_values(["area", "iso3"])
        .reset_index(drop=True)
    )
    return options


def get_country_data(df: pd.DataFrame, iso3: str, year_range: tuple[int, int]) -> pd.DataFrame:
    """
    Filter the panel data for one country and selected year range.
    """
    start_year, end_year = year_range

    out = df.loc[df["iso3"] == iso3].copy()
    out = out.loc[(out["year"] >= start_year) & (out["year"] <= end_year)]
    out = out.sort_values("year")
    return out


# =====================================
# 3. Figure creation
# =====================================

def make_figure(
    df: pd.DataFrame,
    column: str,
    title: str,
    y_label: str,
    line_color: str,
):
    """
    Create one Plotly time-series figure for a selected indicator.
    """
    chart_df = df[["year", column]].copy()

    chart_df["year"] = pd.to_numeric(chart_df["year"], errors="coerce")
    chart_df[column] = pd.to_numeric(chart_df[column], errors="coerce")
    chart_df = (
        chart_df
        .dropna(subset=["year", column])
        .sort_values("year")
        .reset_index(drop=True)
    )

    if chart_df.empty:
        return None

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=chart_df["year"].tolist(),
            y=chart_df[column].tolist(),
            mode="lines+markers",
            line=dict(color=line_color, width=3),
            marker=dict(color=line_color, size=6),
            name=column,
        )
    )

    fig.update_layout(
        title=title,
        height=320,
        paper_bgcolor="black",
        plot_bgcolor="black",
        font=dict(color="#e2e8f0"),
        title_x=0.5,
        hovermode="x unified",
        margin=dict(l=40, r=20, t=60, b=40),
        xaxis=dict(
            title="Year",
            showgrid=True,
            gridcolor="#334155",
            zeroline=False,
            showline=True,
            linecolor="#94a3b8",
            tickfont=dict(color="#e2e8f0"),
        ),
        yaxis=dict(
            title=y_label,
            showgrid=True,
            gridcolor="#334155",
            zeroline=False,
            showline=True,
            linecolor="#94a3b8",
            tickfont=dict(color="#e2e8f0"),
        ),
        showlegend=False,
    )

    return fig


# =====================================
# 4. Streamlit page layout
# =====================================

st.set_page_config(
    page_title="Macro Viewer",
    page_icon="📈",
    layout="wide",
)

st.markdown(
    """
    <style>
    .stApp {
        background-color: #353536;
        color: #e2e8f0;
    }
    .main {
        background-color: #353536;
    }
    section[data-testid="stSidebar"] {
        background-color: black;
    }
    h1, h2, h3, h4, h5, h6, p, div, span, label {
        color: #e2e8f0;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Load all data first
df = load_data(DATA_PATH)
country_options = get_country_options(df)

# Default country index
default_index = 0
if DEFAULT_ISO3 in country_options["iso3"].values:
    default_index = int(country_options.index[country_options["iso3"] == DEFAULT_ISO3][0])

# Year range for sidebar slider
year_series = df["year"].dropna()
if year_series.empty:
    st.error("No valid year data found.")
    st.stop()

min_year = int(year_series.min())
max_year = int(year_series.max())

# Sidebar controls
st.sidebar.header("Controls")

selected_iso3 = st.sidebar.selectbox(
    "Country",
    options=country_options["iso3"].tolist(),
    index=default_index,
    format_func=lambda x: (
        country_options.loc[country_options["iso3"] == x, "area"].iloc[0] + f" ({x})"
    ),
)

selected_year_range = st.sidebar.slider(
    "Year range",
    min_value=min_year,
    max_value=max_year,
    value=(min_year, max_year),
    step=1,
)

view_mode = st.radio(
    "Data source",
    ["FAOSTAT", "WDI", "All"],
    horizontal=True,
)

selected_area = country_options.loc[
    country_options["iso3"] == selected_iso3, "area"
].iloc[0]

st.title(f"Macro Statistics Viewer: {selected_area}")
st.caption("Trial Streamlit app for FAOSTAT and WDI based country panel browsing")


# =====================================
# 5. Filter data for selected country
# =====================================

country_df = get_country_data(df, selected_iso3, selected_year_range)

if country_df.empty:
    st.error("No data found for the selected country and year range.")
    st.stop()


# =====================================
# 6. Determine which indicators to display
# =====================================

chart_columns = list(CHART_SPECS.keys())
available_chart_columns = [c for c in chart_columns if c in country_df.columns]

if view_mode != "All":
    available_chart_columns = [
        c for c in available_chart_columns
        if CHART_SPECS[c]["source"] == view_mode
    ]

if not available_chart_columns:
    st.warning("No indicators available for the selected view.")
    st.stop()

st.subheader(f"{view_mode} indicators" if view_mode != "All" else "All indicators")


# =====================================
# 7. Display charts in two-column layout
# =====================================

def get_line_color(source_name: str) -> str:
    """
    Return a line color by data source.
    """
    if source_name == "FAOSTAT":
        return "orange"   # rose / crimson
    if source_name == "WDI":
        return "green"   # green
    return "#38bdf8"       # fallback blue


col1, col2 = st.columns(2)

for i, column in enumerate(available_chart_columns):
    spec = CHART_SPECS[column]
    line_color = get_line_color(spec["source"])

    fig = make_figure(
        country_df,
        column=column,
        title=spec["title"],
        y_label=spec["label"],
        line_color=line_color,
    )

    if fig is not None:
        if i % 2 == 0:
            col1.plotly_chart(fig, use_container_width=True, theme=None)
        else:
            col2.plotly_chart(fig, use_container_width=True, theme=None)