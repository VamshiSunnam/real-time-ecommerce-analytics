import streamlit as st
import pandas as pd
import plotly.express as px
from dashboard.auth import is_authenticated, login
from consumers.aggregation_engine import db_pool

def fetch_data():
    """Fetch hourly sales data from the database"""
    conn = db_pool.getconn()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT hour_timestamp, total_revenue, total_orders, unique_customers, avg_order_value FROM hourly_sales ORDER BY hour_timestamp DESC")
            data = cursor.fetchall()
            return pd.DataFrame(data, columns=["Hour", "Total Revenue", "Total Orders", "Unique Customers", "Average Order Value"])
    finally:
        db_pool.putconn(conn)

def main():
    """Display the hourly sales page"""
    if not is_authenticated():
        login()
        return

    st.title("Hourly Sales")
    
    df = fetch_data()
    
    if df.empty:
        st.warning("No data available yet. Please wait for events to be processed.")
        return

    # Display line chart
    fig = px.line(df, x="Hour", y="Total Revenue", title="Total Revenue by Hour")
    st.plotly_chart(fig, use_container_width=True)

    # Display data table
    st.dataframe(df)

if __name__ == "__main__":
    main()
