from pathlib import Path
import sqlite3

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "data" / "tradeflow.db"

print("Database path:", DB_PATH)
print("Exists:", DB_PATH.exists())

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

print("\nFirst 10 trades:")
for row in cursor.execute("SELECT trade_id, status FROM trades LIMIT 10"):
    print(row)

conn.close()