from pathlib import Path

DATA_PATH = Path(__file__).resolve().parent / "country_panel.parquet"
DEFAULT_ISO3 = "ZMB"

NUMERIC_COLUMNS = [
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