from pathlib import Path
import sqlite3

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "data" / "tradeflow.db"


def validate_trade(trade_id):
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            trade_date,
            settle_date,
            security_id,
            counterparty_id,
            buy_sell,
            quantity,
            price,
            status
        FROM trades
        WHERE trade_id = ?
        """,
        (trade_id,),
    )

    trade = cursor.fetchone()

    if trade is None:
        connection.close()
        return "Trade not found"

    (
        trade_date,
        settle_date,
        security_id,
        counterparty_id,
        buy_sell,
        quantity,
        price,
        status,
    ) = trade

    cursor.execute(
        "SELECT 1 FROM counterparties WHERE counterparty_id = ?",
        (counterparty_id,),
    )

    if cursor.fetchone() is None:
        connection.close()
        return "Counterparty not found"

    cursor.execute(
        "SELECT 1 FROM securities WHERE security_id = ?",
        (security_id,),
    )

    if cursor.fetchone() is None:
        connection.close()
        return "Security not found"

    if quantity <= 0:
        connection.close()
        return "Invalid quantity"

    if price <= 0:
        connection.close()
        return "Invalid price"

    if settle_date < trade_date:
        connection.close()
        return "Invalid settlement date"

    if buy_sell not in ("BUY", "SELL"):
        connection.close()
        return "Invalid side"

    connection.close()
    return "Validation successful"