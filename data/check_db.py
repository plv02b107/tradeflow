from pathlib import Path
import sqlite3

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "data" / "tradeflow.db"
connection = sqlite3.connect(DB_PATH)



cursor = connection.cursor()

for table in ["counterparties", "securities", "trades"]:
    print(f"\n{table.upper()}")
    rows = cursor.execute(f"SELECT * FROM {table}").fetchall()
    for row in rows:
        print(row)

connection.close()