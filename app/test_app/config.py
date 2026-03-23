from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / "country_panel.parquet"
GROUP_INFO_PATH = BASE_DIR / "country_aggregation_groups.json"

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
    "fertilizer_consumption_kg_per_ha",
]

TIME_SERIES_INDICATORS = {
    "gdp_per_capita_2015": {
        "label": "GDP per Capita",
        "unit": "2015 USD",
        "hover_label": "GDP per capita",
        "log_allowed": True,
        "growth_allowed": True,
        "value_format": ":,.0f",
    },
    "population_total": {
        "label": "Population",
        "unit": "persons",
        "hover_label": "Population",
        "log_allowed": True,
        "growth_allowed": True,
        "value_format": ":,.0f",
    },
    "crop_land_ha": {
        "label": "Cropland",
        "unit": "ha",
        "hover_label": "Cropland",
        "log_allowed": True,
        "growth_allowed": True,
        "value_format": ":,.0f",
    },
    "share_irrigated_percent": {
        "label": "Share of Irrigated Area",
        "unit": "%",
        "hover_label": "Irrigated share",
        "log_allowed": False,
        "growth_allowed": False,
        "value_format": ":.2f",
    },
    "agri_labor": {
        "label": "Agricultural Labor",
        "unit": "persons",
        "hover_label": "Agricultural labor",
        "log_allowed": True,
        "growth_allowed": True,
        "value_format": ":,.0f",
    },
    "fertilizer_consumption_kg_per_ha": {
        "label": "Fertilizer Consumption per Hectare",
        "unit": "kg/ha",
        "hover_label": "Fertilizer consumption per hectare",
        "log_allowed": True,
        "growth_allowed": True,
        "value_format": ":,.0f",
    },
}