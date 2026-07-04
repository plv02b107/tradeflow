from utils.database import get_trades
import streamlit as st

st.set_page_config(page_title="Trades", layout="wide")

st.title("📑 Trade Explorer")

df = get_trades()

# -----------------------
# Search
# -----------------------

search = st.text_input(
    "Search Trade ID",
    "",
)

if search:
    df = df[
        df["trade_id"].str.contains(
            search,
            case=False,
        )
    ]

# -----------------------
# Filters
# -----------------------

col1, col2, col3 = st.columns(3)

status = col1.multiselect(
    "Status",
    sorted(df.status.unique()),
    default=sorted(df.status.unique()),
)

symbol = col2.multiselect(
    "Security",
    sorted(df.symbol.unique()),
    default=sorted(df.symbol.unique()),
)

side = col3.multiselect(
    "Side",
    sorted(df.buy_sell.unique()),
    default=sorted(df.buy_sell.unique()),
)

df = df[
    df.status.isin(status)
]

df = df[
    df.symbol.isin(symbol)
]

df = df[
    df.buy_sell.isin(side)
]

# -----------------------
# KPIs
# -----------------------

c1, c2, c3 = st.columns(3)

c1.metric(
    "Trades",
    len(df),
)

c2.metric(
    "Total Notional",
    f"${df.trade_value.sum():,.2f}",
)

c3.metric(
    "Average Trade",
    f"${df.trade_value.mean():,.2f}",
)

st.divider()

# -----------------------
# Largest Trades
# -----------------------

st.subheader("Top 20 Largest Trades")

largest = df.sort_values(
    "trade_value",
    ascending=False,
).head(20)

st.dataframe(
    largest,
    use_container_width=True,
)

st.divider()

# -----------------------
# Download
# -----------------------

csv = df.to_csv(index=False)

st.download_button(
    "⬇ Download CSV",
    csv,
    "trades.csv",
    "text/csv",
)

st.divider()

st.subheader("All Trades")

st.dataframe(
    df,
    use_container_width=True,
)