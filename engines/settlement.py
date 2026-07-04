from pathlib import Path
import sqlite3
from datetime import datetime

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "data" / "tradeflow.db"


def create_break(cursor, trade_id, reason):
    """
    Creates a settlement break if one does not already exist.
    """

    break_id = f"BRK_{trade_id}"

    exists = cursor.execute(
        """
        SELECT 1
        FROM breaks
        WHERE break_id = ?
        """,
        (break_id,),
    ).fetchone()

    if exists:
        return

    cursor.execute(
        """
        INSERT INTO breaks (
            break_id,
            trade_id,
            break_type,
            description,
            detected_date,
            status
        )
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            break_id,
            trade_id,
            "Settlement",
            reason,
            datetime.today().date(),
            "OPEN",
        ),
    )


def settle_trade(trade_id, success=True):

    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    trade = cursor.execute(
        """
        SELECT
            settle_date,
            quantity,
            price,
            status
        FROM trades
        WHERE trade_id = ?
        """,
        (trade_id,),
    ).fetchone()

    if trade is None:
        connection.close()
        return "Trade not found."

    settle_date, quantity, price, trade_status = trade

    if trade_status != "MATCHED":
        connection.close()
        return f"Trade cannot be settled. Current status : {trade_status}"

    existing = cursor.execute(
        """
        SELECT 1
        FROM settlements
        WHERE trade_id = ?
        """,
        (trade_id,),
    ).fetchone()

    if existing:
        connection.close()
        return "Settlement already exists."

    settlement_amount = quantity * price

    if success:

        settlement_status = "SETTLED"
        new_trade_status = "SETTLED"
        actual_date = datetime.today().date()
        fail_reason = None

    else:

        settlement_status = "FAILED"
        new_trade_status = "FAILED"
        actual_date = None
        fail_reason = "Insufficient funds"

    cursor.execute(
        """
        INSERT INTO settlements (
            settlement_id,
            trade_id,
            expected_date,
            actual_date,
            settlement_amount,
            status,
            fail_reason
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (
            f"SET_{trade_id}",
            trade_id,
            settle_date,
            actual_date,
            settlement_amount,
            settlement_status,
            fail_reason,
        ),
    )

    cursor.execute(
        """
        UPDATE trades
        SET status = ?
        WHERE trade_id = ?
        """,
        (
            new_trade_status,
            trade_id,
        ),
    )

    if not success:
        create_break(
            cursor,
            trade_id,
            fail_reason,
        )

    connection.commit()
    connection.close()

    if success:
        return "Trade settled successfully."

    return "Settlement failed."