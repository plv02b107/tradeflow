from pathlib import Path
import sqlite3

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "data" / "tradeflow.db"


def add_counterparty(counterparty_id, name, counterparty_type, country):
    connection = sqlite3.connect(DB_PATH)

    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO counterparties (
            counterparty_id,
            name,
            type,
            country
        )
        VALUES (?, ?, ?, ?)
        """,
        (
            counterparty_id,
            name,
            counterparty_type,
            country,
        ),
    )

    connection.commit()
    connection.close()


def add_security(
    security_id,
    symbol,
    security_name,
    asset_class,
    currency,
    exchange,
):
    connection = sqlite3.connect(DB_PATH)

    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO securities (
            security_id,
            symbol,
            security_name,
            asset_class,
            currency,
            exchange
        )
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            security_id,
            symbol,
            security_name,
            asset_class,
            currency,
            exchange,
        ),
    )

    connection.commit()
    connection.close()