import requests
import pandas as pd
import streamlit as st
import plotly.express as px


BACKEND = "http://localhost:8000"


st.set_page_config(
    page_title="API Tracker",
    page_icon="📊",
    layout="wide"
)


st.title("📊 API Usage Tracker")


# --------------------------------------------------
# Get summary
# --------------------------------------------------

try:

    summary = requests.get(
        f"{BACKEND}/usage/summary",
        timeout=5
    ).json()

except Exception:

    st.error(
        "Cannot connect to API Tracker backend."
    )

    st.stop()


# --------------------------------------------------
# Metrics
# --------------------------------------------------

col1, col2, col3, col4, col5 = (
    st.columns(5)
)


col1.metric(
    "Requests",
    summary["requests"]
)

col2.metric(
    "Input Tokens",
    f"{summary['input_tokens']:,}"
)

col3.metric(
    "Output Tokens",
    f"{summary['output_tokens']:,}"
)

col4.metric(
    "Total Cost",
    f"${summary['total_cost']:.4f}"
)

col5.metric(
    "Avg Latency",
    f"{summary['average_latency_ms']:.0f} ms"
)


st.divider()


# --------------------------------------------------
# Usage
# --------------------------------------------------

try:

    data = requests.get(
        f"{BACKEND}/usage/",
        timeout=5
    ).json()

except Exception:

    st.error(
        "Unable to retrieve usage."
    )

    st.stop()


if not data:

    st.info(
        "No API usage recorded yet."
    )

    st.stop()


df = pd.DataFrame(data)
st.write("API Response:")
st.json(data)

st.write("DataFrame columns:")
st.write(df.columns.tolist())

st.write("DataFrame:")
st.dataframe(df)

# --------------------------------------------------
# Cost by project
# --------------------------------------------------

st.subheader(
    "Cost by Project"
)


project_cost = (
    df.groupby("project")[
        "total_cost"
    ]
    .sum()
    .reset_index()
)


fig = px.bar(
    project_cost,
    x="project",
    y="total_cost",
    title="API Cost by Project"
)

st.plotly_chart(
    fig,
    use_container_width=True
)


# --------------------------------------------------
# Cost by provider
# --------------------------------------------------

st.subheader(
    "Cost by Provider"
)


provider_cost = (
    df.groupby("provider")[
        "total_cost"
    ]
    .sum()
    .reset_index()
)


fig2 = px.pie(
    provider_cost,
    names="provider",
    values="total_cost",
    title="Cost Distribution"
)

st.plotly_chart(
    fig2,
    use_container_width=True
)


# --------------------------------------------------
# Usage table
# --------------------------------------------------

st.subheader(
    "Recent API Calls"
)


display_columns = [
    "timestamp",
    "project",
    "provider",
    "model",
    "input_tokens",
    "output_tokens",
    "total_tokens",
    "total_cost",
    "latency_ms",
    "status"
]


st.dataframe(
    df[display_columns],
    use_container_width=True
)