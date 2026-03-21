from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]
DATA_PATH = BASE_DIR / "data" / "raw" / "country_panel.csv"
DOCS_DIR = BASE_DIR / "docs"