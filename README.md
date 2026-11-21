# Customer Loyalty & Reward Reconciliation System

A data-driven dashboard designed to monitor customer loyalty points, track reward redemptions, identify expired points, and detect discrepancies in customer reward balances.

## Live Demo

**[Open Customer Loyalty & Reward Reconciliation Dashboard](https://customer-loyalty-reconciliation-yn9dvzhlcewwhhbvavxpy3.streamlit.app/)**

## Project Overview

The Customer Loyalty & Reward Reconciliation System helps businesses monitor and reconcile customer loyalty reward points.

The application uses customer purchase records, redemption records, and expiry records to calculate expected loyalty balances and compare them with recorded balances. It identifies discrepancies and provides an interactive dashboard for reviewing customer-level records.

## Key Features

- **Dashboard Overview:** Displays total customers, purchases, points earned, points redeemed, points expired, and discrepancies.
- **Balance Reconciliation:** Compares customer loyalty balances and identifies mismatched records.
- **Redemption Analysis:** Tracks redeemed points and highlights the top 10 customers by redemption.
- **Expiry Analysis:** Monitors expired reward points and identifies customers with the highest expired points.
- **Customer Audit Trail:** Provides customer-level purchase, redemption, expiry, and balance records.
- **Interactive Visualizations:** Presents reconciliation results and reward-point analysis through charts and tables.
- **Database Integration:** Connects to Neon PostgreSQL to retrieve and display stored records.

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| Pandas | Data processing and analysis |
| Streamlit | Interactive web application |
| Plotly | Data visualization |
| PostgreSQL | Relational database |
| Neon | Cloud-hosted PostgreSQL database |
| SQLAlchemy | Database connectivity |
| GitHub | Source code management |
| Streamlit Community Cloud | Application deployment |
| Google Colab | Development and notebook environment |

## Project Architecture

```text
        Data Generation
              |
              v
       Python + Pandas
              |
              v
       Neon PostgreSQL
              |
              v
        SQLAlchemy
              |
              v
       Streamlit App
              |
              v
       Plotly Charts
              |
              v
       Interactive Dashboard
```

## Database Tables

The project uses the following database tables:

| Table | Description |
|---|---|
| customers | Customer profile and membership information |
| purchases | Customer purchase and earned-point records |
| redemptions | Redeemed loyalty-point records |
| expiry | Expired loyalty-point records |
| balances | Calculated customer loyalty balances and reconciliation status |
| audit_report | Customer-level reconciliation report |

## Application Modules

### 1. Dashboard
Provides an overall summary of customer activity and loyalty-point statistics.

### 2. Reconciliation
Displays calculated customer balances and identifies records with discrepancies.

### 3. Redemption Analysis
Analyzes redeemed reward points and displays the top customers by redemption.

### 4. Expiry Analysis
Displays expired reward points and customer-level expiry records.

### 5. Customer Audit Trail
Allows users to select a customer and inspect their profile, purchases, redemptions, expiry records, and audit report.

## Installation and Setup

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/customer-loyalty-reconciliation.git
```

```bash
cd customer-loyalty-reconciliation
```

Replace `YOUR_USERNAME` with your GitHub username.

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Database Connection

Create a `.streamlit/secrets.toml` file:

```toml
DATABASE_URL = "your_neon_database_connection_string"
```

Replace the placeholder with your actual Neon PostgreSQL connection string.

**Security:** Never commit `secrets.toml` or expose your database credentials publicly.

### 4. Run the Application

```bash
streamlit run app.py
```

The application will start locally in your browser.

## Deployment

The application is deployed using **Streamlit Community Cloud**.

- Source code: GitHub
- Database: Neon PostgreSQL
- Hosting: Streamlit Community Cloud

The database connection is configured through Streamlit Secrets.

## Dataset

The
