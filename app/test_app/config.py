from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / "country_panel.parquet"
CROP_DATA_PATH = BASE_DIR / "country_crop_year.parquet"
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

CROP_NUMERIC_COLUMNS = [
    "item_code",
    "crop_name",
    "year",
    "production_ton",
    "yield_kg_per_ha",
    "area_harvested_ha",
    "stocks_ton",
    "gross_production_value_current_usd",
    "gross_production_value_constant_2014_2016_usd",
    "producer_price_usd_per_tonne",
    "producer_price_index_2014_2016",
    "import_quantity_ton",
    "import_value_usd",
    "export_quantity_ton",
    "export_value_usd",
    "food_supply_kg_capita_yr",
    "food_supply_kcal_capita_day",
    "protein_supply_g_capita_day",
    "fat_supply_g_capita_day"
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
    "cereal_yield_kg_per_ha": {
        "label": "Cereal Yield",
        "unit": "kg/ha",
        "hover_label": "Cereal yield",
        "log_allowed": True,
        "growth_allowed": True,
        "value_format": ":,.0f",
    },
}

CROSS_SECTION_SCATTERS = [
    {
        "title": "Fertilizer Consumption - Share of Irrigated Area",
        "x": "fertilizer_consumption_kg_per_ha",
        "y": "share_irrigated_percent",
        "x_label": "Fertilizer Consumption (kg/ha)",
        "y_label": "Share of Irrigated Area (%)",
        "x_format": ".2f",
        "y_format": ".2f",
        "size": "crop_land_ha",
        "key_prefix": "scatter1",
    },
    {
        "title": "Fertilizer Consumption - Crop Land",
        "x": "fertilizer_consumption_kg_per_ha",
        "y": "crop_land_ha",
        "x_label": "Fertilizer Consumption (kg/ha)",
        "y_label": "Crop Land (ha)",
        "x_format": ".2f",
        "y_format": ".2f",
        "size": None,
        "key_prefix": "scatter2",
    },
    {
        "title": "Cereal Yield - Fertilizer Consumption",
        "x": "fertilizer_consumption_kg_per_ha",
        "y": "cereal_yield_kg_per_ha",
        "x_label": "Fertilizer Consumption (kg/ha)",
        "y_label": "Cereal Yield (kg/ha)",
        "x_format": ".2f",
        "y_format": ".2f",
        "size": "crop_land_ha",
        "key_prefix": "scatter3",
    },
    {
        "title": "Agricultural GDP Share - GDP per Capita",
        "x": "gdp_per_capita_2015",
        "y": "agri_gdp_share_percent",
        "x_label": "GDP per Capita (2015 USD)",
        "y_label": "Agricultural GDP Share (%)",
        "x_format": ".2f",
        "y_format": ".2f",
        "size": None,
        "key_prefix": "scatter4",
    },
]