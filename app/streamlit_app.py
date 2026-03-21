from pathlib import Path

import pandas as pd
import plotly.graph_objects as go
import streamlit as st


# =====================================
# 1. Basic paths and app-level settings
# =====================================

BASE_DIR = Path(__file__).resolve().parents[1]
DATA_PATH = BASE_DIR / "data" / "raw" / "country_panel.csv"

TARGET_ISO3 = "ZMB"

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
        "source": "FAOSTAT",
    },
    "agri_gdp_share_percent": {
        "label": "Agricultural GDP share (%)",
        "title": "Agricultural GDP share",
        "source": "FAOSTAT",
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


def get_country_data(df: pd.DataFrame, iso3: str) -> pd.DataFrame:
    out = df.loc[df["iso3"] == iso3].copy()
    out = out.sort_values("year")
    return out


# =====================================
# 3. Figure creation
# =====================================

def make_figure(df: pd.DataFrame, column: str, title: str, y_label: str):
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
            line=dict(color="#f43f5e", width=3),
            marker=dict(color="#f43f5e", size=6),
            name=column,
        )
    )

    fig.update_layout(
        title=title,
        height=320,
        paper_bgcolor="#0f172a",
        plot_bgcolor="#0f172a",
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

st.title("Macro Statistics Viewer")
st.caption("Trial Streamlit app for FAOSTAT and WDI based country panel browsing")

view_mode = st.radio(
    "Data source",
    ["FAOSTAT", "WDI", "All"],
    horizontal=True,
)


# =====================================
# 5. Load country data
# =====================================

df = load_data(DATA_PATH)
zmb = get_country_data(df, TARGET_ISO3)

if zmb.empty:
    st.error("No Zambia data found.")
    st.stop()


# =====================================
# 6. Overview charts
# =====================================

st.subheader(f"{view_mode} indicators" if view_mode != "All" else "All indicators")

chart_columns = list(CHART_SPECS.keys())
available_chart_columns = [c for c in chart_columns if c in zmb.columns]

if view_mode != "All":
    available_chart_columns = [
        c for c in available_chart_columns
        if CHART_SPECS[c]["source"] == view_mode
    ]

col1, col2 = st.columns(2)

for i, column in enumerate(available_chart_columns):
    spec = CHART_SPECS[column]

    fig = make_figure(
        zmb,
        column=column,
        title=spec["title"],
        y_label=spec["label"],
    )

    if fig is not None:
        if i % 2 == 0:
            col1.plotly_chart(fig, use_container_width=True, theme=None)
        else:
            col2.plotly_chart(fig, use_container_width=True, theme=None)