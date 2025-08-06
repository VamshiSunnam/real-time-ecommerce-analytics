import streamlit as st
import pandas as pd
import plotly.express as px
from dashboard.auth import is_authenticated, login
from consumers.aggregation_engine import db_pool

def fetch_data():
    """Fetch real-time metrics from the database"""
    conn = db_pool.getconn()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT metric_name, metric_value, time_window FROM real_time_metrics ORDER BY created_at DESC LIMIT 100")
            data = cursor.fetchall()
            return pd.DataFrame(data, columns=["Metric Name", "Value", "Time Window"])
    finally:
        db_pool.putconn(conn)

def main():
    """Display the real-time metrics page"""
    if not is_authenticated():
        login()
        return

    st.title("Real-time Metrics")
    
    df = fetch_data()
    
    if df.empty:
        st.warning("No data available yet. Please wait for events to be processed.")
        return

    # Display key metrics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Sales (Last Hour)", f"${df[df['Metric Name'] == 'total_sales']['Value'].iloc[0]:,.2f}")
    with col2:
        st.metric("Total Orders (Last Hour)", f"{df[df['Metric Name'] == 'total_orders']['Value'].iloc[0]:,}")
    with col3:
        st.metric("Unique Customers (Last Hour)", f"{df[df['Metric Name'] == 'unique_customers']['Value'].iloc[0]:,}")

    # Display data table
    st.dataframe(df)

if __name__ == "__main__":
    main()
