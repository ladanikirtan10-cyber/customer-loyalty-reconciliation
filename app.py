
import streamlit as st
import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine

# Page settings
st.set_page_config(
    page_title="Loyalty Reconciliation",
    page_icon="🎁",
    layout="wide"
)

# Connect to Neon database
database_url = st.secrets["DATABASE_URL"]

database_url = database_url.replace(
    "postgresql://",
    "postgresql+psycopg://"
)

engine = create_engine(database_url)

# Dashboard title
st.title("Customer Loyalty & Reward Reconciliation")
st.write("Customer loyalty management dashboard")

# Read database tables
customers = pd.read_sql("SELECT * FROM customers", engine)
balances = pd.read_sql("SELECT * FROM balances", engine)
purchases = pd.read_sql("SELECT * FROM purchases", engine)

# Dashboard numbers
col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Customers", len(customers))

col2.metric("Total Purchases", len(purchases))

col3.metric("Points Earned", int(purchases["points_earned"].sum()))

col4.metric(
    "Discrepancies",
    int((balances["status"] == "Discrepancy").sum())
)

# Customer table
st.subheader("Customer Loyalty Records")
st.dataframe(balances, use_container_width=True)

# Discrepancy chart
st.subheader("Reconciliation Summary")

chart = px.pie(
    balances,
    names="status",
    title="Matched vs Discrepancy"
)

st.plotly_chart(chart, use_container_width=True)

st.success("Dashboard loaded successfully!")
