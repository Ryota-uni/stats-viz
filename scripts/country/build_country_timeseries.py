import plotly.express as px

from scripts.common.paths import DATA_PATH, DOCS_DIR
from scripts.common.utils import load_country_panel, get_zambia_country_panel


CHART_SPECS = [
    {
        "column": "crop_land_ha",
        "title": "Zambia: Crop land area over time",
        "y_label": "Crop land (ha)",
        "output": "zambia_crop_land.html",
    },
    {
        "column": "share_irrigated_percent",
        "title": "Zambia: Share of irrigated agricultural land over time",
        "y_label": "Irrigated share (%)",
        "output": "zambia_irrigation_share.html",
    },
    {
        "column": "agri_labor",
        "title": "Zambia: Agricultural labor over time",
        "y_label": "Agricultural labor",
        "output": "zambia_agri_labor.html",
    },
    {
        "column": "fertilizer_total_ton",
        "title": "Zambia: Fertilizer use over time",
        "y_label": "Fertilizer total (ton)",
        "output": "zambia_fertilizer_total.html",
    },
    {
        "column": "net_capital_2015",
        "title": "Zambia: Net capital stock over time",
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
        title_x=0.5,
        hovermode="x unified",
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