from utils.database import get_breaks
import streamlit as st
import plotly.express as px

st.set_page_config(page_title="Breaks", layout="wide")

st.title("🚨 Break Management")

df = get_breaks()

c1, c2 = st.columns(2)

c1.metric(
    "Open Breaks",
    (df.status == "OPEN").sum(),
)

c2.metric(
    "Resolved",
    (df.status == "RESOLVED").sum(),
)

st.divider()

status = (
    df.break_type
    .value_counts()
    .reset_index()
)

status.columns = [
    "Break Type",
    "Count",
]

fig = px.bar(
    status,
    x="Break Type",
    y="Count",
    title="Break Types",
)

st.plotly_chart(
    fig,
    use_container_width=True,
)

st.divider()

open_breaks = df[
    df.status == "OPEN"
]

st.subheader("Open Breaks")

st.dataframe(
    open_breaks,
    use_container_width=True,
)

st.divider()

st.subheader("All Breaks")

st.dataframe(
    df,
    use_container_width=True,
)