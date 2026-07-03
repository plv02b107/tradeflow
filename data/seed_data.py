from pathlib import Path
import sqlite3

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "data" / "tradeflow.db"

connection = sqlite3.connect(DB_PATH)
cursor = connection.cursor()

cursor.execute("""
INSERT INTO counterparties
VALUES ('CP001','Goldman Sachs','Broker','USA')
""")

cursor.execute("""
INSERT INTO securities
VALUES ('SEC001','AAPL','Apple Inc.','Equity','USD','NASDAQ')
""")

connection.commit()
connection.close()

print("Reference data inserted.")