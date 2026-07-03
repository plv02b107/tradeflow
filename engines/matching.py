from pathlib import Path
import sqlite3

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "data" / "tradeflow.db"


def match_trade(trade_id):
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT security_id, counterparty_id, status
        FROM trades
        WHERE trade_id = ?
        """,
        (trade_id,),
    )

    trade = cursor.fetchone()

    if trade is None:
        connection.close()
        return False

    security_id, counterparty_id, status = trade

    if status != "CAPTURED":
        connection.close()
        return False

    cursor.execute(
        "SELECT 1 FROM securities WHERE security_id = ?",
        (security_id,),
    )

    if cursor.fetchone() is None:
        connection.close()
        return False

    cursor.execute(
        "SELECT 1 FROM counterparties WHERE counterparty_id = ?",
        (counterparty_id,),
    )

    if cursor.fetchone() is None:
        connection.close()
        return False

    cursor.execute(
        """
        UPDATE trades
        SET status = 'MATCHED'
        WHERE trade_id = ?
        """,
        (trade_id,),
    )

    connection.commit()
    connection.close()

    return True