from utils.database import get_settlements
import streamlit as st
import plotly.express as px

st.set_page_config(page_title="Settlements", layout="wide")

st.title("💰 Settlement Monitor")

df = get_settlements()

c1, c2, c3 = st.columns(3)

c1.metric(
    "Settlements",
    len(df),
)

c2.metric(
    "Successful",
    (df.status == "SETTLED").sum(),
)

c3.metric(
    "Failed",
    (df.status == "FAILED").sum(),
)

st.divider()

status = (
    df.status
    .value_counts()
    .reset_index()
)

status.columns = [
    "Status",
    "Count",
]

fig = px.bar(
    status,
    x="Status",
    y="Count",
    title="Settlement Status",
)

st.plotly_chart(
    fig,
    use_container_width=True,
)

st.divider()

failed = df[df.status == "FAILED"]

st.subheader("Failed Settlements")

st.dataframe(
    failed,
    use_container_width=True,
)

st.divider()

st.subheader("All Settlements")

st.dataframe(
    df,
    use_container_width=True,
)