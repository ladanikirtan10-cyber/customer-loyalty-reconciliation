
import streamlit as st
import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine, text

# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="Customer Loyalty Reconciliation",
    page_icon="🎁",
    layout="wide"
)

# --------------------------------------------------
# DATABASE CONNECTION
# --------------------------------------------------

@st.cache_resource
def get_engine():
    database_url = st.secrets["DATABASE_URL"]
    database_url = database_url.replace(
        "postgresql://",
        "postgresql+psycopg://",
        1
    )
    return create_engine(database_url)

engine = get_engine()


@st.cache_data(ttl=60)
def load_data():
    with engine.connect() as connection:
        customers = pd.read_sql_query(
            text("SELECT * FROM customers"), connection
        )
        purchases = pd.read_sql_query(
            text("SELECT * FROM purchases"), connection
        )
        redemptions = pd.read_sql_query(
            text("SELECT * FROM redemptions"), connection
        )
        expiry = pd.read_sql_query(
            text("SELECT * FROM expiry"), connection
        )
        balances = pd.read_sql_query(
            text("SELECT * FROM balances"), connection
        )
        audit_report = pd.read_sql_query(
            text("SELECT * FROM audit_report"), connection
        )

    return customers, purchases, redemptions, expiry, balances, audit_report


# --------------------------------------------------
# LOAD DATABASE TABLES
# --------------------------------------------------

try:
    (
        customers,
        purchases,
        redemptions,
        expiry,
        balances,
        audit_report
    ) = load_data()

except Exception as error:
    st.error("Unable to connect to the database or load the records.")
    st.code(str(error))
    st.stop()


# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

st.sidebar.title("🎁 Loyalty System")

page = st.sidebar.radio(
    "Navigation",
    [
        "Dashboard",
        "Reconciliation",
        "Redemption Analysis",
        "Expiry Analysis",
        "Customer Audit Trail"
    ]
)

if st.sidebar.button("Refresh Data"):
    st.cache_data.clear()
    st.rerun()


# --------------------------------------------------
# DASHBOARD
# --------------------------------------------------

if page == "Dashboard":

    st.title("Customer Loyalty & Reward Reconciliation")
    st.write(
        "Monitor customer purchases, reward points, "
        "redemptions, expiry events and balance discrepancies."
    )

    total_customers = len(customers)
    total_purchases = len(purchases)
    total_earned = int(purchases["points_earned"].sum())
    total_redeemed = int(redemptions["points_redeemed"].sum())
    total_expired = int(expiry["points_expired"].sum())
    discrepancies = int(
        (balances["status"] == "Discrepancy").sum()
    )

    st.subheader("Key Performance Indicators")

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Customers", f"{total_customers:,}")
    col2.metric("Total Purchases", f"{total_purchases:,}")
    col3.metric("Points Earned", f"{total_earned:,}")

    col4, col5, col6 = st.columns(3)

    col4.metric("Points Redeemed", f"{total_redeemed:,}")
    col5.metric("Points Expired", f"{total_expired:,}")
    col6.metric("Discrepancies", f"{discrepancies:,}")

    st.divider()

    st.subheader("Reconciliation Overview")

    chart = px.pie(
        balances,
        names="status",
        title="Matched vs Discrepancy",
        hole=0.4
    )

    st.plotly_chart(chart, use_container_width=True)

    st.subheader("Customer Balance Records")
    st.dataframe(balances, use_container_width=True)


# --------------------------------------------------
# RECONCILIATION
# --------------------------------------------------

elif page == "Reconciliation":

    st.title("Balance Reconciliation")

    st.write(
        "Compare calculated loyalty balances with recorded balances "
        "to identify discrepancies."
    )

    status_filter = st.selectbox(
        "Filter by Status",
        ["All", "Matched", "Discrepancy"]
    )

    filtered_balances = balances.copy()

    if status_filter != "All":
        filtered_balances = filtered_balances[
            filtered_balances["status"] == status_filter
        ]

    st.dataframe(
        filtered_balances,
        use_container_width=True
    )

    st.subheader("Discrepancy Records")

    discrepancy_data = balances[
        balances["status"] == "Discrepancy"
    ]

    if discrepancy_data.empty:
        st.success("No discrepancies found.")
    else:
        st.warning(
            f"{len(discrepancy_data)} customer records have discrepancies."
        )
        st.dataframe(
            discrepancy_data,
            use_container_width=True
        )


# --------------------------------------------------
# REDEMPTION ANALYSIS
# --------------------------------------------------

elif page == "Redemption Analysis":

    st.title("Redemption Analysis")

    total_redeemed = int(
        redemptions["points_redeemed"].sum()
    )

    st.metric("Total Points Redeemed", f"{total_redeemed:,}")

    st.subheader("Redemption Records")

    st.dataframe(
        redemptions,
        use_container_width=True
    )

    top_customers = (
        redemptions.groupby("customer_id")["points_redeemed"]
        .sum()
        .reset_index()
        .sort_values("points_redeemed", ascending=False)
        .head(10)
    )

    st.subheader("Top 10 Customers by Points Redeemed")

    chart = px.bar(
        top_customers,
        x="customer_id",
        y="points_redeemed",
        title="Top Customers by Redemption",
        labels={
            "customer_id": "Customer ID",
            "points_redeemed": "Points Redeemed"
        }
    )

    st.plotly_chart(chart, use_container_width=True)


# --------------------------------------------------
# EXPIRY ANALYSIS
# --------------------------------------------------

elif page == "Expiry Analysis":

    st.title("Expiry Analysis")

    total_expired = int(
        expiry["points_expired"].sum()
    )

    st.metric("Total Expired Points", f"{total_expired:,}")

    st.subheader("Expiry Records")

    st.dataframe(
        expiry,
        use_container_width=True
    )

    top_expiry = (
        expiry.groupby("customer_id")["points_expired"]
        .sum()
        .reset_index()
        .sort_values("points_expired", ascending=False)
        .head(10)
    )

    st.subheader("Top 10 Customers by Expired Points")

    chart = px.bar(
        top_expiry,
        x="customer_id",
        y="points_expired",
        title="Top Customers by Expired Points",
        labels={
            "customer_id": "Customer ID",
            "points_expired": "Points Expired"
        }
    )

    st.plotly_chart(chart, use_container_width=True)


# --------------------------------------------------
# CUSTOMER AUDIT TRAIL
# --------------------------------------------------

elif page == "Customer Audit Trail":

    st.title("Customer Audit Trail")

    st.write(
        "Select a customer to inspect their profile, "
        "purchases, redemptions, expiry events and balance."
    )

    customer_options = customers["customer_id"].tolist()

    selected_customer = st.selectbox(
        "Select Customer ID",
        customer_options
    )

    customer_profile = customers[
        customers["customer_id"] == selected_customer
    ]

    customer_balance = balances[
        balances["customer_id"] == selected_customer
    ]

    customer_purchases = purchases[
        purchases["customer_id"] == selected_customer
    ]

    customer_redemptions = redemptions[
        redemptions["customer_id"] == selected_customer
    ]

    customer_expiry = expiry[
        expiry["customer_id"] == selected_customer
    ]

    st.subheader("Customer Profile")
    st.dataframe(customer_profile, use_container_width=True)

    st.subheader("Loyalty Balance")
    st.dataframe(customer_balance, use_container_width=True)

    st.subheader("Purchase History")
    st.dataframe(customer_purchases, use_container_width=True)

    st.subheader("Redemption History")
    st.dataframe(customer_redemptions, use_container_width=True)

    st.subheader("Expiry History")
    st.dataframe(customer_expiry, use_container_width=True)

    st.subheader("Audit Report")
    customer_audit = audit_report[
        audit_report["customer_id"] == selected_customer
    ]

    st.dataframe(customer_audit, use_container_width=True)


# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.divider()

st.caption(
    "Customer Loyalty & Reward Reconciliation System | "
    "Powered by Streamlit and Neon PostgreSQL"
)
