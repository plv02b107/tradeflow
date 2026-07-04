from pathlib import Path

import plotly.express as px
import streamlit as st

from utils.database import (
    get_breaks,
    get_settlements,
    get_trades,
)

st.set_page_config(
    page_title="TradeFlow",
    page_icon="📈",
    layout="wide",
)

st.title("📈 TradeFlow")
st.caption("Post-Trade Operations Dashboard")

# -------------------------
# Load Data
# -------------------------

trades = get_trades()
settlements = get_settlements()
breaks = get_breaks()

# -------------------------
# Sidebar Filters
# -------------------------

st.sidebar.header("Filters")

status_filter = st.sidebar.multiselect(
    "Trade Status",
    sorted(trades["status"].unique()),
    default=sorted(trades["status"].unique()),
)

security_filter = st.sidebar.multiselect(
    "Security",
    sorted(trades["symbol"].unique()),
    default=sorted(trades["symbol"].unique()),
)

counterparty_filter = st.sidebar.multiselect(
    "Counterparty",
    sorted(trades["counterparty_name"].unique()),
    default=sorted(trades["counterparty_name"].unique()),
)

side_filter = st.sidebar.multiselect(
    "Buy / Sell",
    sorted(trades["buy_sell"].unique()),
    default=sorted(trades["buy_sell"].unique()),
)

filtered = trades[
    (trades["status"].isin(status_filter))
    & (trades["symbol"].isin(security_filter))
    & (trades["counterparty_name"].isin(counterparty_filter))
    & (trades["buy_sell"].isin(side_filter))
]

# -------------------------
# KPI Calculations
# -------------------------

total_trades = len(filtered)

matched = (filtered["status"] == "MATCHED").sum()

settled = (filtered["status"] == "SETTLED").sum()

failed = (filtered["status"] == "FAILED").sum()

open_breaks = (breaks["status"] == "OPEN").sum()

total_notional = filtered["trade_value"].sum()

avg_trade = filtered["trade_value"].mean()

settlement_success = (
    settled / total_trades * 100
    if total_trades
    else 0
)

failed_rate = (
    failed / total_trades * 100
    if total_trades
    else 0
)

# -------------------------
# KPI Row 1
# -------------------------

c1, c2, c3, c4, c5 = st.columns(5)

c1.metric("Trades", f"{total_trades:,}")

c2.metric("Matched", matched)

c3.metric("Settled", settled)

c4.metric("Failed", failed)

c5.metric("Open Breaks", open_breaks)

# -------------------------
# KPI Row 2
# -------------------------

c6, c7, c8, c9 = st.columns(4)

c6.metric(
    "Total Notional",
    f"${total_notional:,.2f}",
)

c7.metric(
    "Average Trade",
    f"${avg_trade:,.2f}",
)

c8.metric(
    "Settlement Success %",
    f"{settlement_success:.1f}%",
)

c9.metric(
    "Failure Rate",
    f"{failed_rate:.1f}%",
)

st.divider()

# -------------------------
# Charts
# -------------------------

left, right = st.columns(2)

trade_status = (
    filtered["status"]
    .value_counts()
    .reset_index()
)

trade_status.columns = [
    "Status",
    "Count",
]

fig1 = px.pie(
    trade_status,
    names="Status",
    values="Count",
    title="Trade Status",
)

left.plotly_chart(
    fig1,
    use_container_width=True,
)

settlement_status = (
    settlements["status"]
    .value_counts()
    .reset_index()
)

settlement_status.columns = [
    "Status",
    "Count",
]

fig2 = px.bar(
    settlement_status,
    x="Status",
    y="Count",
    title="Settlement Status",
)

right.plotly_chart(
    fig2,
    use_container_width=True,
)

# -------------------------
# Row 2 Charts
# -------------------------

left2, right2 = st.columns(2)

break_status = (
    breaks["break_type"]
    .value_counts()
    .reset_index()
)

break_status.columns = [
    "Break Type",
    "Count",
]

fig3 = px.bar(
    break_status,
    x="Break Type",
    y="Count",
    title="Break Analysis",
)

left2.plotly_chart(
    fig3,
    use_container_width=True,
)

daily = (
    filtered.groupby("trade_date")
    .size()
    .reset_index(name="Trades")
)

fig4 = px.line(
    daily,
    x="trade_date",
    y="Trades",
    markers=True,
    title="Daily Trade Volume",
)

right2.plotly_chart(
    fig4,
    use_container_width=True,
)

st.divider()

# -------------------------
# Top Trades
# -------------------------

st.subheader("Largest Trades")

largest = filtered.sort_values(
    "trade_value",
    ascending=False,
).head(10)

st.dataframe(
    largest[
        [
            "trade_id",
            "symbol",
            "counterparty_name",
            "buy_sell",
            "quantity",
            "price",
            "trade_value",
            "status",
        ]
    ],
    use_container_width=True,
)

st.divider()

# -------------------------
# Complete Table
# -------------------------

st.subheader("Trade Inventory")

st.dataframe(
    filtered,
    use_container_width=True,
)