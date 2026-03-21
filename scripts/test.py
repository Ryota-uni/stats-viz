from pathlib import Path

import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots


BASE_DIR = Path(__file__).resolve().parents[1]
DATA_PATH = BASE_DIR / "data" / "raw" / "country_panel.csv"
DOCS_DIR = BASE_DIR / "docs"
OUTPUT_PATH = DOCS_DIR / "zambia_overview.html"


def main() -> None:
    df = pd.read_csv(DATA_PATH)

    zmb = (
        df.loc[
            df["iso3"] == "ZMB",
            ["year", "crop_land_ha", "share_irrigated_percent"]
        ]
        .dropna(subset=["year"])
        .sort_values("year")
        .copy()
    )

    if zmb.empty:
        raise ValueError("No Zambia data found.")

    # table 用には直近10年だけ使う
    table_df = zmb.tail(10).copy()

    fig = make_subplots(
        rows=3,
        cols=1,
        shared_xaxes=True,
        vertical_spacing=0.06,
        row_heights=[0.34, 0.33, 0.33],
        specs=[
            [{"type": "table"}],
            [{"type": "scatter"}],
            [{"type": "scatter"}],
        ],
        subplot_titles=(
            "Recent data table",
            "Crop land area",
            "Share of irrigated agricultural land",
        ),
    )

    # Table
    fig.add_trace(
        go.Table(
            header=dict(
                values=["Year", "Crop land (ha)", "Irrigated share (%)"],
                align="left",
            ),
            cells=dict(
                values=[
                    table_df["year"].tolist(),
                    table_df["crop_land_ha"].round(2).tolist(),
                    table_df["share_irrigated_percent"].round(2).tolist(),
                ],
                align="left",
            ),
        ),
        row=1,
        col=1,
    )

    # Crop land
    fig.add_trace(
        go.Scatter(
            x=zmb["year"],
            y=zmb["crop_land_ha"],
            mode="lines+markers",
            name="crop_land_ha",
        ),
        row=2,
        col=1,
    )

    # Irrigation share
    fig.add_trace(
        go.Scatter(
            x=zmb["year"],
            y=zmb["share_irrigated_percent"],
            mode="lines+markers",
            name="share_irrigated_percent",
        ),
        row=3,
        col=1,
    )

    fig.update_layout(
        height=900,
        title="Zambia overview",
        template="plotly_white",
        showlegend=False,
    )

    DOCS_DIR.mkdir(parents=True, exist_ok=True)
    fig.write_html(OUTPUT_PATH, include_plotlyjs="cdn", full_html=True)

    print(f"Saved: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()