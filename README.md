# TradeFlow

TradeFlow is a Python-based simulation of a post-trade operations platform used in investment banking and capital markets.

The project models the lifecycle of an equity trade after execution, including trade capture, validation, matching, settlement, reconciliation, and break management. It also includes a Streamlit dashboard for monitoring operational KPIs and trade activity.

The goal of this project was to better understand how operations teams manage post-trade workflows while building a modular Python application with a relational database and reporting layer.

---

## Dashboard

### Live Dashboard

![Dashboard Demo](docs/dashboard_demo.gif)

### Dashboard Screenshots

#### Overview

![Overview](docs/dashboard.png)

#### Trade Inventory

![Trades](docs/trades.png)

#### Settlement Monitoring

![Settlements](docs/settlements.png)

#### Break Management

![Breaks](docs/breaks.png)

---

## System Architecture

![Architecture](docs/architecture.png)

---

## Features

### Trade Capture

- Capture equity trades
- Store trade records in SQLite
- Maintain security and counterparty master data

### Trade Validation

- Validate mandatory fields
- Reject invalid trades
- Apply business rules before processing

### Trade Matching

- Match validated trades
- Update trade lifecycle status

### Settlement

- Simulate successful and failed settlements
- Calculate settlement amounts
- Record settlement status and failure reasons

### Reconciliation

- Compare trade and settlement records
- Detect settlement mismatches

### Break Management

- Automatically create operational breaks
- Track unresolved exceptions
- Monitor failed settlements

### Operations Dashboard

- Interactive Streamlit dashboard
- Trade inventory
- Settlement monitoring
- Counterparty exposure
- Daily trade volume
- Operational KPIs

---

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

---

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
├── docs/
│   ├── architecture.png
│   ├── dashboard_demo.gif
│   ├── dashboard.png
│   ├── trades.png
│   ├── settlements.png
│   └── breaks.png
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

---

## Database

TradeFlow uses SQLite to store the complete trade lifecycle.

Main tables include:

- trades
- settlements
- counterparties
- securities
- breaks

Sample data is generated automatically to simulate realistic operational workflows.

---

## Tech Stack

- Python
- SQLite
- Streamlit
- Pandas
- Plotly
- Faker

---

## Getting Started

Clone the repository.

```bash
git clone https://github.com/<your-username>/tradeflow.git
cd tradeflow
```

Create a virtual environment.

```bash
python -m venv venv
```

Activate it.

### Windows

```bash
venv\Scripts\activate
```

Install dependencies.

```bash
pip install -r requirements.txt
```

Initialize the database.

```bash
python engines/init_db.py
```

Generate sample data.

```bash
python data/generate_sample_data.py
```

Run the dashboard.

```bash
streamlit run dashboard/app.py
```

---

## Sample Data

The project generates realistic operational data for demonstration purposes.

The dataset includes:

- 500+ simulated equity trades
- Settlement records
- Successful and failed settlements
- Operational breaks
- Security master data
- Counterparty master data

This allows the dashboard and reporting modules to be tested without relying on external market data.

---

## What I Learned

Building TradeFlow helped me understand how post-trade operations work inside financial institutions.

Some of the concepts explored during the project include:

- Equity trade lifecycle
- Trade validation
- Trade matching
- Settlement processing
- Reconciliation
- Operational break management
- Relational database design
- Building analytical dashboards with Streamlit
- Writing modular and maintainable Python code

---

## Future Improvements

Planned enhancements include:

- Trade search and advanced filtering
- CSV and Excel trade import
- Break resolution workflow
- User authentication
- Audit logging
- REST API
- Docker deployment
- Historical reporting
- Role-based dashboards

---

## License

This project is intended for educational and portfolio purposes.
