import pandas as pd


def load_country_panel(path) -> pd.DataFrame:
    df = pd.read_csv(path)
    if "year" in df.columns:
        df["year"] = pd.to_numeric(df["year"], errors="coerce")
    return df


def get_zambia_country_panel(df: pd.DataFrame) -> pd.DataFrame:
    zmb = df.loc[df["iso3"] == "ZMB"].copy()
    zmb = zmb.sort_values("year")
    return zmb