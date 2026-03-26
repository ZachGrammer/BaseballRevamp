from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from pathlib import Path
import pandas as pd
import os

load_dotenv()

engine = create_engine(os.getenv("NEON_DB_URL"))
print("Connected setup ready.")

BASE_DIR = Path(__file__).resolve().parents[1]
sql_dir = BASE_DIR / "sql"
data_file = BASE_DIR / "data" / "final" / "player_season_summary.parquet"

with engine.begin() as conn:
    with open(sql_dir / "01_create_schema.sql", "r", encoding="utf-8") as f:
        conn.execute(text(f.read()))
print("Schema created.")

with engine.begin() as conn:
    with open(sql_dir / "02_create_tables.sql", "r", encoding="utf-8") as f:
        conn.execute(text(f.read()))
print("Table created.")

season_summary = pd.read_parquet(data_file)

season_summary.columns = [
    c.strip().lower().replace(" ", "_").replace("-", "_")
    for c in season_summary.columns
]

season_summary = season_summary.rename(columns={
    "woba_denom": "woba_denom_value",
    "pa": "pa_count",
    "hbp": "hbp_event",
    "h": "hit",
    "1b": "single",
    "2b": "double",
    "3b": "triple",
    "hr": "home_run"
})

season_summary = season_summary[[
    "season",
    "batter",

    "pa_count",
    "woba_denom_value",

    "expected_numerator",
    "actual_numerator",

    "xwoba",
    "woba",
    "woba_minus_xwoba",
    "xwoba_minus_woba",

    "bb",
    "ibb",
    "hbp_event",
    "sf",
    "ab",
    "hit",
    "single",
    "double",
    "triple",
    "home_run"
]]

season_summary.to_sql(
    name="player_season_summary",
    con=engine,
    schema="analytics",
    if_exists="append",
    index=False,
    method="multi",
    chunksize=5000
)

print("Data uploaded.")