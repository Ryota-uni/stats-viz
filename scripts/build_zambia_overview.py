from pathlib import Path
import pandas as pd
import plotly.express as px


BASE_DIR = Path(__file__).resolve().parents[1]
DATA_PATH = BASE_DIR / "data" / "raw" / "country_panel.csv"
DOCS_DIR = BASE_DIR / "docs"


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
]


def build_line_chart(df: pd.DataFrame, column: str, title: str, y_label: str, output_name: str) -> None:
    chart_df = (
        df.loc[df["iso3"] == "ZMB", ["year", column]]
        .dropna()
        .sort_values("year")
    )

    if chart_df.empty:
        raise ValueError(f"No Zambia data found for column='{column}'.")

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

    DOCS_DIR.mkdir(parents=True, exist_ok=True)
    fig.write_html(
        DOCS_DIR / output_name,
        include_plotlyjs="cdn",
        full_html=True,
    )


def build_index() -> None:
    html = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>Zambia Stats Viz</title>
</head>
<body>
  <h1>Zambia Stats Visualization</h1>
  <ul>
    <li><a href="./zambia_crop_land.html">Zambia crop land</a></li>
    <li><a href="./zambia_irrigation_share.html">Zambia irrigation share</a></li>
  </ul>
</body>
</html>
"""
    (DOCS_DIR / "index.html").write_text(html, encoding="utf-8")


def main() -> None:
    df = pd.read_csv(DATA_PATH)

    for spec in CHART_SPECS:
        build_line_chart(
            df=df,
            column=spec["column"],
            title=spec["title"],
            y_label=spec["y_label"],
            output_name=spec["output"],
        )

    build_index()
    print("Charts and index page have been generated in docs/.")


if __name__ == "__main__":
    main()