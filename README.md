# TradeFlow

TradeFlow is a Python-based simulation of a post-trade operations platform used in capital markets. It models the complete lifecycle of an equity trade, from trade capture to settlement, while tracking operational exceptions through reconciliation and break management.

The project was built to understand how operations teams process trades after execution and to gain practical experience with the trade lifecycle used by investment banks and financial institutions.

## Features

- Trade Capture
  - Capture equity trades and store them in SQLite.
  - Maintain counterparty and security master data.

- Trade Validation
  - Validate trade details before processing.
  - Reject invalid or incomplete trades.

- Trade Matching
  - Match captured trades and update trade status.

- Settlement Engine
  - Simulate successful and failed settlements.
  - Record settlement amounts and settlement status.

- Reconciliation
  - Compare trade and settlement records.
  - Detect mismatches automatically.

- Break Management
  - Create operational breaks for failed settlements.
  - Track open reconciliation breaks.

- Operations Dashboard
  - Built using Streamlit.
  - View trades, settlements and operational KPIs.
  - Interactive tables and visualizations.

## Project Structure

```
tradeflow/
│
├── dashboard/
│   ├── app.py
│   └── pages/
│
├── data/
│   ├── schema.sql
│   ├── seed_data.py
│   ├── generate_sample_data.py
│   └── tradeflow.db
│
├── engines/
│   ├── capture.py
│   ├── validation.py
│   ├── matching.py
│   ├── settlement.py
│   ├── reconciliation.py
│   ├── master_data.py
│   └── init_db.py
│
├── tests/
│
├── requirements.txt
└── README.md
```

## Tech Stack

- Python
- SQLite
- Streamlit
- Pandas
- Plotly

## Database

The project uses SQLite with the following tables:

- counterparties
- securities
- trades
- settlements
- breaks

The schema models a simplified post-trade processing workflow.

## Trade Lifecycle

```
Trade Capture
      │
      ▼
Trade Validation
      │
      ▼
Trade Matching
      │
      ▼
Settlement
      │
      ├── Success
      │       │
      │       ▼
      │   Trade Settled
      │
      └── Failure
              │
              ▼
      Reconciliation
              │
              ▼
      Break Management
```

## Running the Project

Clone the repository

```bash
git clone <repository-url>
cd tradeflow
```

Create a virtual environment

```bash
python -m venv venv
```

Activate it

Windows

```bash
venv\Scripts\activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

Initialize the database

```bash
python engines/init_db.py
```

Generate sample data

```bash
python data/generate_sample_data.py
```

Run the dashboard

```bash
streamlit run dashboard/app.py
```

## Sample Data

The generator creates realistic operational data including

- Counterparties
- Securities
- Equity trades
- Settlement records
- Failed settlements
- Operational breaks

This makes it possible to test reporting and dashboard functionality without external data sources.

## What I Learned

While building this project, I gained hands-on experience with

- The equity trade lifecycle
- Trade validation and matching
- Settlement processing
- Reconciliation workflows
- Operational exception handling
- Relational database design
- Building dashboards with Streamlit
- Writing modular Python applications

## Future Improvements

- CSV trade import
- Trade search and filtering
- Break resolution workflow
- User authentication
- Audit logging
- REST API
- Docker support
