from pathlib import Path
import sqlite3
from datetime import datetime

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "data" / "tradeflow.db"


def create_break(cursor, trade_id, break_type, description):
    """
    Creates a break if it does not already exist.
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
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            break_id,
            trade_id,
            break_type,
            description,
            datetime.today().date(),
            "OPEN",
        ),
    )


def match_trade(trade_id):

    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    trade = cursor.execute(
        """
        SELECT
            security_id,
            counterparty_id,
            status
        FROM trades
        WHERE trade_id = ?
        """,
        (trade_id,),
    ).fetchone()

    if trade is None:
        connection.close()
        return "Trade not found."

    security_id, counterparty_id, status = trade

    if status == "MATCHED":
        connection.close()
        return "Trade already matched."

    if status == "SETTLED":
        connection.close()
        return "Trade already settled."

    if status == "FAILED":
        connection.close()
        return "Trade has failed validation."

    security = cursor.execute(
        """
        SELECT 1
        FROM securities
        WHERE security_id = ?
        """,
        (security_id,),
    ).fetchone()

    if security is None:

        create_break(
            cursor,
            trade_id,
            "Matching",
            "Security not found",
        )

        cursor.execute(
            """
            UPDATE trades
            SET status='FAILED'
            WHERE trade_id=?
            """,
            (trade_id,),
        )

        connection.commit()
        connection.close()

        return "Matching failed : Security not found."

    cp = cursor.execute(
        """
        SELECT 1
        FROM counterparties
        WHERE counterparty_id = ?
        """,
        (counterparty_id,),
    ).fetchone()

    if cp is None:

        create_break(
            cursor,
            trade_id,
            "Matching",
            "Counterparty not found",
        )

        cursor.execute(
            """
            UPDATE trades
            SET status='FAILED'
            WHERE trade_id=?
            """,
            (trade_id,),
        )

        connection.commit()
        connection.close()

        return "Matching failed : Counterparty not found."

    cursor.execute(
        """
        UPDATE trades
        SET status='MATCHED'
        WHERE trade_id=?
        """,
        (trade_id,),
    )

    connection.commit()
    connection.close()

    return "Trade matched successfully."