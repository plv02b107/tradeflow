from pathlib import Path
import sqlite3

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "data" / "tradeflow.db"


def reconcile_trade(trade_id):
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    trade = cursor.execute(
        """
        SELECT status
        FROM trades
        WHERE trade_id = ?
        """,
        (trade_id,),
    ).fetchone()

    settlement = cursor.execute(
        """
        SELECT status
        FROM settlements
        WHERE trade_id = ?
        """,
        (trade_id,),
    ).fetchone()

    if trade and settlement:
        if trade[0] == "SETTLED" and settlement[0] == "SETTLED":
            print("No reconciliation breaks found.")
        else:
            cursor.execute(
                """
                INSERT INTO breaks (
                    break_id,
                    trade_id,
                    break_type,
                    description,
                    detected_date
                )
                VALUES (?, ?, ?, ?, DATE('now'))
                """,
                (
                    f"BRK_{trade_id}",
                    trade_id,
                    "Settlement",
                    "Trade and settlement status mismatch",
                ),
            )
            connection.commit()
            print("Reconciliation break created.")

    connection.close()