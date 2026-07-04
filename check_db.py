from pathlib import Path
import sqlite3

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "data" / "tradeflow.db"

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

print("\nTrades")

for row in cursor.execute(
    """
    SELECT status, COUNT(*)
    FROM trades
    GROUP BY status
    """
):
    print(row)

print("\nSettlements")

for row in cursor.execute(
    """
    SELECT status, COUNT(*)
    FROM settlements
    GROUP BY status
    """
):
    print(row)

print("\nBreaks")

for row in cursor.execute(
    """
    SELECT status, COUNT(*)
    FROM breaks
    GROUP BY status
    """
):
    print(row)

conn.close()