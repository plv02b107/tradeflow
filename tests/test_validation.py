from pathlib import Path
import sqlite3
from datetime import datetime

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "data" / "tradeflow.db"


def create_break(cursor, trade_id, break_type, description):
    """
    Creates a break only if one doesn't already exist.
    """

    break_id = f"BRK_{trade_id}_{break_type.upper()}"

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
        VALUES (?, ?, ?, ?, ?, 'OPEN')
        """,
        (
            break_id,
            trade_id,
            break_type,
            description,
            datetime.today().date(),
        ),
    )


def fail_trade(cursor, trade_id):
    cursor.execute(
        """
        UPDATE trades
        SET status='FAILED'
        WHERE trade_id=?
        """,
        (trade_id,),
    )


def validate_trade(trade_id):

    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    trade = cursor.execute(
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
        WHERE trade_id=?
        """,
        (trade_id,),
    ).fetchone()

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

    if status != "CAPTURED":
        connection.close()
        return f"Trade already {status}"

    security = cursor.execute(
        """
        SELECT 1
        FROM securities
        WHERE security_id=?
        """,
        (security_id,),
    ).fetchone()

    if security is None:
        fail_trade(cursor, trade_id)

        create_break(
            cursor,
            trade_id,
            "Reference Data",
            "Security does not exist",
        )

        connection.commit()
        connection.close()

        return "Validation Failed : Invalid Security"

    cp = cursor.execute(
        """
        SELECT 1
        FROM counterparties
        WHERE counterparty_id=?
        """,
        (counterparty_id,),
    ).fetchone()

    if cp is None:

        fail_trade(cursor, trade_id)

        create_break(
            cursor,
            trade_id,
            "Reference Data",
            "Counterparty does not exist",
        )

        connection.commit()
        connection.close()

        return "Validation Failed : Invalid Counterparty"

    if quantity <= 0:

        fail_trade(cursor, trade_id)

        create_break(
            cursor,
            trade_id,
            "Validation",
            "Quantity must be positive",
        )

        connection.commit()
        connection.close()

        return "Validation Failed : Invalid Quantity"

    if price <= 0:

        fail_trade(cursor, trade_id)

        create_break(
            cursor,
            trade_id,
            "Validation",
            "Price must be positive",
        )

        connection.commit()
        connection.close()

        return "Validation Failed : Invalid Price"

    if settle_date < trade_date:

        fail_trade(cursor, trade_id)

        create_break(
            cursor,
            trade_id,
            "Validation",
            "Settlement date before trade date",
        )

        connection.commit()
        connection.close()

        return "Validation Failed : Invalid Settlement Date"

    if buy_sell not in ("BUY", "SELL"):

        fail_trade(cursor, trade_id)

        create_break(
            cursor,
            trade_id,
            "Validation",
            "Invalid Buy/Sell side",
        )

        connection.commit()
        connection.close()

        return "Validation Failed : Invalid Side"

    connection.commit()
    connection.close()

    return "Validation Successful"