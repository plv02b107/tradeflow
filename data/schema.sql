PRAGMA foreign_keys = ON;

CREATE TABLE counterparties (
    counterparty_id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    type TEXT NOT NULL,
    country TEXT
);

CREATE TABLE securities (
    security_id TEXT PRIMARY KEY,
    symbol TEXT NOT NULL,
    security_name TEXT NOT NULL,
    asset_class TEXT NOT NULL,
    currency TEXT NOT NULL,
    exchange TEXT
);

CREATE TABLE trades (
    trade_id TEXT PRIMARY KEY,
    trade_date DATE NOT NULL,
    settle_date DATE NOT NULL,
    security_id TEXT NOT NULL,
    counterparty_id TEXT NOT NULL,
    buy_sell TEXT NOT NULL CHECK (buy_sell IN ('BUY','SELL')),
    quantity INTEGER NOT NULL CHECK (quantity > 0),
    price REAL NOT NULL CHECK (price > 0),
    status TEXT DEFAULT 'CAPTURED' CHECK (status IN ('CAPTURED','MATCHED','SETTLED','FAILED')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (security_id) REFERENCES securities(security_id),
    FOREIGN KEY (counterparty_id) REFERENCES counterparties(counterparty_id)
);

CREATE TABLE settlements (
    settlement_id TEXT PRIMARY KEY,
    trade_id TEXT NOT NULL,
    expected_date DATE NOT NULL,
    actual_date DATE,
    settlement_amount REAL,
    status TEXT DEFAULT 'PENDING' CHECK (status IN ('PENDING','SETTLED','FAILED')),
    fail_reason TEXT,
    FOREIGN KEY (trade_id) REFERENCES trades(trade_id)
);


CREATE TABLE breaks (
    break_id TEXT PRIMARY KEY,
    trade_id TEXT NOT NULL,
    break_type TEXT NOT NULL,
    description TEXT,
    detected_date DATE NOT NULL,
    resolved_date DATE,
    status TEXT DEFAULT 'OPEN'
        CHECK(status IN ('OPEN','RESOLVED')),
    FOREIGN KEY (trade_id) REFERENCES trades(trade_id)
);