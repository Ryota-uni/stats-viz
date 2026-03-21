from pathlib import Path
import pandas as pd
import plotly.express as px


BASE_DIR = Path(__file__).resolve().parents[1]
DATA_PATH = BASE_DIR / "data" / "raw" / "country_panel.csv"
DOCS_DIR = BASE_DIR / "docs"
OUTPUT_PATH = DOCS_DIR / "zambia_crop_land.html"


def main() -> None:
    # Read data
    df = pd.read_csv(DATA_PATH)

    # Keep Zambia only
    zmb = (
        df.loc[df["iso3"] == "ZMB", ["year", "crop_land_ha"]]
        .dropna()
        .sort_values("year")
    )

    if zmb.empty:
        raise ValueError("No Zambia data found for iso3='ZMB'.")

    # Build figure
    fig = px.line(
        zmb,
        x="year",
        y="crop_land_ha",
        markers=True,
        title="Zambia: Crop land area over time",
        labels={
            "year": "Year",
            "crop_land_ha": "Crop land (ha)",
        },
    )

    fig.update_layout(
        template="plotly_white",
        title_x=0.5,
        hovermode="x unified",
    )

    # Export HTML
    DOCS_DIR.mkdir(parents=True, exist_ok=True)
    fig.write_html(
        OUTPUT_PATH,
        include_plotlyjs="cdn",
        full_html=True,
    )

    print(f"Saved: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()