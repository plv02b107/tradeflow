from pathlib import Path
import random
import sqlite3
from faker import Faker

fake = Faker()

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "data" / "tradeflow.db"

connection = sqlite3.connect(DB_PATH)
cursor = connection.cursor()

counterparties = [
    ("CP001", "Goldman Sachs", "Broker", "USA"),
    ("CP002", "JPMorgan Chase", "Broker", "USA"),
    ("CP003", "Morgan Stanley", "Broker", "USA"),
    ("CP004", "Barclays", "Broker", "UK"),
    ("CP005", "HSBC", "Broker", "UK"),
    ("CP006", "UBS", "Broker", "Switzerland"),
    ("CP007", "Nomura", "Broker", "Japan"),
    ("CP008", "Deutsche Bank", "Broker", "Germany"),
    ("CP009", "BNP Paribas", "Broker", "France"),
    ("CP010", "Citi", "Broker", "USA"),
]

for row in counterparties:
    cursor.execute(
        """
        INSERT OR IGNORE INTO counterparties
        VALUES (?,?,?,?)
        """,
        row,
    )

securities = [
    ("SEC001", "AAPL", "Apple Inc.", "Equity", "USD", "NASDAQ"),
    ("SEC002", "MSFT", "Microsoft", "Equity", "USD", "NASDAQ"),
    ("SEC003", "GOOGL", "Alphabet", "Equity", "USD", "NASDAQ"),
    ("SEC004", "AMZN", "Amazon", "Equity", "USD", "NASDAQ"),
    ("SEC005", "NVDA", "NVIDIA", "Equity", "USD", "NASDAQ"),
    ("SEC006", "META", "Meta", "Equity", "USD", "NASDAQ"),
    ("SEC007", "TSLA", "Tesla", "Equity", "USD", "NASDAQ"),
    ("SEC008", "NFLX", "Netflix", "Equity", "USD", "NASDAQ"),
    ("SEC009", "IBM", "IBM", "Equity", "USD", "NYSE"),
    ("SEC010", "ORCL", "Oracle", "Equity", "USD", "NYSE"),
]

for row in securities:
    cursor.execute(
        """
        INSERT OR IGNORE INTO securities
        VALUES (?,?,?,?,?,?)
        """,
        row,
    )

security_ids = [row[0] for row in securities]
counterparty_ids = [row[0] for row in counterparties]

for i in range(1, 501):

    trade_id = f"TRD{i:04d}"
    
    trade_date = str(
    fake.date_between(
        start_date="-60d",
        end_date="-2d",
    )
)

    settle_date = str(
    fake.date_between(
        start_date=trade_date,
        end_date="+3d",
    )
)
    

    security = random.choice(security_ids)
    counterparty = random.choice(counterparty_ids)

    side = random.choice(["BUY", "SELL"])

    quantity = random.randint(50, 5000)

    price = round(random.uniform(20, 500), 2)

    status = random.choices(
        ["CAPTURED", "MATCHED", "SETTLED", "FAILED"],
        weights=[15, 20, 55, 10],
    )[0]

    cursor.execute(
        """
        INSERT OR IGNORE INTO trades(
            trade_id,
            trade_date,
            settle_date,
            security_id,
            counterparty_id,
            buy_sell,
            quantity,
            price,
            status
        )
        VALUES(?,?,?,?,?,?,?,?,?)
        """,
        (
            trade_id,
            trade_date,
            settle_date,
            security,
            counterparty,
            side,
            quantity,
            price,
            status,
        ),
    )

    if status in ["SETTLED", "FAILED"]:

        settlement_id = f"SET_{trade_id}"

        amount = round(quantity * price, 2)

        actual_date = (
            settle_date
            if status == "SETTLED"
            else None
        )

        fail_reason = (
            None
            if status == "SETTLED"
            else random.choice(
                [
                    "Insufficient funds",
                    "Counterparty issue",
                    "Instruction mismatch",
                    "System outage",
                ]
            )
        )

        cursor.execute(
            """
            INSERT OR IGNORE INTO settlements(
                settlement_id,
                trade_id,
                expected_date,
                actual_date,
                settlement_amount,
                status,
                fail_reason
            )
            VALUES(?,?,?,?,?,?,?)
            """,
            (
                settlement_id,
                trade_id,
                settle_date,
                actual_date,
                amount,
                status,
                fail_reason,
            ),
        )

        if status == "FAILED":

            cursor.execute(
                """
                INSERT OR IGNORE INTO breaks(
                    break_id,
                    trade_id,
                    break_type,
                    description,
                    detected_date,
                    status
                )
                VALUES(?,?,?,?,?,?)
                """,
                (
                    f"BRK_{trade_id}",
                    trade_id,
                    "Settlement",
                    fail_reason,
                    fake.date_between(
                        start_date=trade_date,
                        end_date="today",
                    ),
                    "OPEN",
                ),
            )

connection.commit()
connection.close()

print("500 sample trades generated successfully.")