from scripts.common.paths import DOCS_DIR


LINKS = [
    ("Zambia macro table", "zambia_table.html"),
    ("Zambia crop land", "zambia_crop_land.html"),
    ("Zambia irrigation share", "zambia_irrigation_share.html"),
    ("Zambia agricultural labor", "zambia_agri_labor.html"),
    ("Zambia fertilizer total", "zambia_fertilizer_total.html"),
    ("Zambia net capital", "zambia_net_capital.html"),
]


def main() -> None:
    DOCS_DIR.mkdir(parents=True, exist_ok=True)

    items = "\n".join(
        [f'    <li><a href="./{href}">{label}</a></li>' for label, href in LINKS]
    )

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>Zambia Stats Viz</title>
</head>
<body>
  <h1>Zambia Stats Visualization</h1>
  <ul>
{items}
  </ul>
</body>
</html>
"""
    (DOCS_DIR / "index.html").write_text(html, encoding="utf-8")
    print(f"Saved: {DOCS_DIR / 'index.html'}")


if __name__ == "__main__":
    main()