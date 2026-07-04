from pathlib import Path
import sqlite3
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent.parent
DB_PATH = BASE_DIR / "data" / "tradeflow.db"


def get_connection():
    return sqlite3.connect(DB_PATH)


def get_trades():

    conn = get_connection()

    df = pd.read_sql_query(
        """
        SELECT
            t.*,
            s.symbol,
            c.name AS counterparty_name,
            (t.quantity * t.price) AS trade_value
        FROM trades t
        JOIN securities s
            ON t.security_id = s.security_id
        JOIN counterparties c
            ON t.counterparty_id = c.counterparty_id
        """,
        conn,
    )

    conn.close()

    return df


def get_settlements():

    conn = get_connection()

    df = pd.read_sql_query(
        """
        SELECT *
        FROM settlements
        """,
        conn,
    )

    conn.close()

    return df


def get_breaks():

    conn = get_connection()

    df = pd.read_sql_query(
        """
        SELECT *
        FROM breaks
        """,
        conn,
    )

    conn.close()

    return df


def get_counterparties():

    conn = get_connection()

    df = pd.read_sql_query(
        """
        SELECT *
        FROM counterparties
        """,
        conn,
    )

    conn.close()

    return df


def get_securities():

    conn = get_connection()

    df = pd.read_sql_query(
        """
        SELECT *
        FROM securities
        """,
        conn,
    )

    conn.close()

    return df