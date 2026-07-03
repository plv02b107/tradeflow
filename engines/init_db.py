from pathlib import Path
import sqlite3

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "data" / "tradeflow.db"
SCHEMA_PATH = BASE_DIR / "data" / "schema.sql"

if DB_PATH.exists():
    DB_PATH.unlink()

connection = sqlite3.connect(DB_PATH)
with open(SCHEMA_PATH, "r", encoding="utf-8") as file:
    connection.executescript(file.read())
connection.commit()
connection.close()

print("Database initialized successfully.")