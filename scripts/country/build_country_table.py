import pandas as pd

from scripts.common.paths import DATA_PATH, DOCS_DIR
from scripts.common.utils import load_country_panel, get_zambia_country_panel


TABLE_COLUMNS = [
    "year",
    "crop_land_ha",
    "share_irrigated_percent",
    "agri_labor",
    "fertilizer_total_ton",
    "net_capital_2015",
]

COLUMN_LABELS = {
    "year": "Year",
    "crop_land_ha": "Crop land (1000 ha)",
    "share_irrigated_percent": "Irrigated share (%)",
    "agri_labor": "Agricultural labor",
    "fertilizer_total_ton": "Fertilizer total (ton)",
    "net_capital_2015": "Net capital (2015 USD)",
}


def main() -> None:
    df = load_country_panel(DATA_PATH)
    zmb = get_zambia_country_panel(df)

    table_df = zmb[TABLE_COLUMNS].copy()
    table_df = table_df.rename(columns=COLUMN_LABELS)

    DOCS_DIR.mkdir(parents=True, exist_ok=True)

    html_table = table_df.to_html(index=False, classes="dataframe", border=0)

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>Zambia macro table</title>
  <style>
    body {{
      font-family: Arial, sans-serif;
      margin: 40px;
      line-height: 1.5;
    }}
    h1 {{
      margin-bottom: 20px;
    }}
    table {{
      border-collapse: collapse;
      width: 100%;
      font-size: 14px;
    }}
    th, td {{
      border: 1px solid #ddd;
      padding: 8px 10px;
      text-align: right;
    }}
    th:first-child, td:first-child {{
      text-align: center;
    }}
    thead {{
      background-color: #f5f5f5;
    }}
    tr:nth-child(even) {{
      background-color: #fafafa;
    }}
  </style>
</head>
<body>
  <h1>Zambia macro panel table</h1>
  {html_table}
</body>
</html>
"""

    output_path = DOCS_DIR / "zambia_table.html"
    output_path.write_text(html, encoding="utf-8")
    print(f"Saved: {output_path}")


if __name__ == "__main__":
    main()