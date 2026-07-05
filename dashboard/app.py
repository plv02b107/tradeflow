from pathlib import Path
import sqlite3

import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(
    page_title="TradeFlow",
    
    layout="wide",
)

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "data" / "tradeflow.db"

connection = sqlite3.connect(DB_PATH)

trades = pd.read_sql_query(
    """
    SELECT
        t.*,
        s.symbol,
        c.name AS counterparty_name,
        quantity * price AS trade_value
    FROM trades t
    JOIN securities s
        ON t.security_id=s.security_id
    JOIN counterparties c
        ON t.counterparty_id=c.counterparty_id
    """,
    connection,
)

settlements = pd.read_sql_query(
    "SELECT * FROM settlements",
    connection,
)

breaks = pd.read_sql_query(
    "SELECT * FROM breaks",
    connection,
)

connection.close()

# ---------------- Sidebar ----------------

st.sidebar.header("Filters")

status_filter = st.sidebar.multiselect(
    "Trade Status",
    trades["status"].unique(),
    default=list(trades["status"].unique()),
)

counterparty_filter = st.sidebar.multiselect(
    "Counterparty",
    trades["counterparty_name"].unique(),
    default=list(trades["counterparty_name"].unique()),
)

filtered = trades[
    (trades["status"].isin(status_filter))
    &
    (trades["counterparty_name"].isin(counterparty_filter))
]

# ---------------- KPIs ----------------

total_trades = len(filtered)

matched = (filtered["status"] == "MATCHED").sum()

settled = (filtered["status"] == "SETTLED").sum()

failed = (filtered["status"] == "FAILED").sum()

open_breaks = len(breaks)

total_notional = filtered["trade_value"].sum()

average_trade = filtered["trade_value"].mean()

settlement_rate = (
    settled / total_trades * 100
    if total_trades
    else 0
)

failure_rate = (
    failed / total_trades * 100
    if total_trades
    else 0
)

st.title(" TradeFlow")

st.caption("Post-Trade Operations Dashboard")

c1, c2, c3, c4, c5 = st.columns(5)

c1.metric("Trades", f"{total_trades:,}")
c2.metric("Matched", matched)
c3.metric("Settled", settled)
c4.metric("Failed", failed)
c5.metric("Open Breaks", open_breaks)

c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "Total Notional",
    f"${total_notional/1_000_000:.1f}M",
)

c2.metric(
    "Average Trade",
    f"${average_trade:,.0f}",
)

c3.metric(
    "Settlement Success %",
    f"{settlement_rate:.1f}%",
)

c4.metric(
    "Failure Rate",
    f"{failure_rate:.1f}%",
)

st.divider()

# ---------------- Charts ----------------

left, right = st.columns(2)

with left:

    fig = px.pie(
        filtered,
        names="status",
        title="Trade Status",
    )

    st.plotly_chart(
        fig,
        width="stretch",
    )

with right:

    fig = px.bar(
        settlements.groupby("status")
        .size()
        .reset_index(name="Count"),
        x="status",
        y="Count",
        color="status",
        title="Settlement Status",
    )

    st.plotly_chart(
        fig,
        width="stretch",
    )

left, right = st.columns(2)

with left:

    if len(breaks):

        fig = px.bar(
            breaks.groupby("description")
            .size()
            .reset_index(name="Count"),
            x="description",
            y="Count",
            color="description",
            title="Break Reasons",
        )

        st.plotly_chart(
            fig,
            width="stretch",
        )

with right:

    exposure = (
        filtered
        .groupby("counterparty_name")["trade_value"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
        .reset_index()
    )

    fig = px.bar(
        exposure,
        x="counterparty_name",
        y="trade_value",
        title="Counterparty Exposure",
    )

    st.plotly_chart(
        fig,
        width="stretch",
    )

daily = (
    filtered
    .groupby("trade_date")
    .size()
    .reset_index(name="Trades")
)

fig = px.line(
    daily,
    x="trade_date",
    y="Trades",
    markers=True,
    title="Daily Trade Volume",
)

st.plotly_chart(
    fig,
    width="stretch",
)