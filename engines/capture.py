from pathlib import Path
import sqlite3

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "data" / "tradeflow.db"


def capture_trade(
    trade_id,
    trade_date,
    settle_date,
    security_id,
    counterparty_id,
    buy_sell,
    quantity,
    price,
):
    connection = sqlite3.connect(DB_PATH)

    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO trades (
            trade_id,
            trade_date,
            settle_date,
            security_id,
            counterparty_id,
            buy_sell,
            quantity,
            price
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            trade_id,
            trade_date,
            settle_date,
            security_id,
            counterparty_id,
            buy_sell,
            quantity,
            price,
        ),
    )

    connection.commit()
    connection.close()