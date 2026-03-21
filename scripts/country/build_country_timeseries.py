import plotly.express as px

from scripts.common.paths import DATA_PATH, DOCS_DIR
from scripts.common.utils import load_country_panel, get_zambia_country_panel


CHART_SPECS = [
    {
        "column": "crop_land_ha",
        "title": "Crop land area",
        "y_label": "Crop land (1000 ha)",
        "output": "zambia_crop_land.html",
    },
    {
        "column": "share_irrigated_percent",
        "title": "Share of irrigated agricultural",
        "y_label": "Irrigated share (%)",
        "output": "zambia_irrigation_share.html",
    },
    {
        "column": "agri_labor",
        "title": "Agricultural labor",
        "y_label": "Agricultural labor",
        "output": "zambia_agri_labor.html",
    },
    {
        "column": "fertilizer_total_ton",
        "title": "Fertilizer use",
        "y_label": "Fertilizer total (ton)",
        "output": "zambia_fertilizer_total.html",
    },
    {
        "column": "net_capital_2015",
        "title": "Net capital stock",
        "y_label": "Net capital (2015 USD)",
        "output": "zambia_net_capital.html",
    },
]


def build_chart(zmb, column: str, title: str, y_label: str, output: str) -> None:
    chart_df = zmb[["year", column]].dropna().copy()

    if chart_df.empty:
        print(f"Skipped: {column} has no data.")
        return

    fig = px.line(
        chart_df,
        x="year",
        y=column,
        markers=True,
        title=title,
        labels={
            "year": "Year",
            column: y_label,
        },
    )

    fig.update_layout(
        template="plotly_white",
        paper_bgcolor="navy",
        plot_bgcolor="navy",
        font=dict(color="#e2e8f0"),
        title_x=0.5,
        hovermode="x unified",
        xaxis=dict(
            gridcolor="#334155",
            zerolinecolor="#334155",
        ),
        yaxis=dict(
            gridcolor="#334155",
            zerolinecolor="#334155",
        ),
    )

    fig.update_traces(
        line=dict(color="crimson", width=3),
        marker=dict(color="crimson", size=6),
    )

    fig.write_html(
        DOCS_DIR / output,
        include_plotlyjs="cdn",
        full_html=True,
    )
    print(f"Saved: {DOCS_DIR / output}")


def main() -> None:
    df = load_country_panel(DATA_PATH)
    zmb = get_zambia_country_panel(df)

    DOCS_DIR.mkdir(parents=True, exist_ok=True)

    for spec in CHART_SPECS:
        build_chart(
            zmb=zmb,
            column=spec["column"],
            title=spec["title"],
            y_label=spec["y_label"],
            output=spec["output"],
        )


if __name__ == "__main__":
    main()