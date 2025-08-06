import streamlit as st
import pandas as pd
import plotly.express as px
from dashboard.auth import is_authenticated, login
from consumers.aggregation_engine import db_pool

def fetch_data():
    """Fetch product performance data from the database"""
    conn = db_pool.getconn()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT product_name, total_sales, total_views, conversion_rate FROM product_performance ORDER BY total_sales DESC")
            data = cursor.fetchall()
            return pd.DataFrame(data, columns=["Product Name", "Total Sales", "Total Views", "Conversion Rate"])
    finally:
        db_pool.putconn(conn)

def main():
    """Display the product performance page"""
    if not is_authenticated():
        login()
        return

    st.title("Product Performance")
    
    df = fetch_data()
    
    if df.empty:
        st.warning("No data available yet. Please wait for events to be processed.")
        return

    # Display bar chart
    fig = px.bar(df, x="Product Name", y="Total Sales", title="Total Sales by Product")
    st.plotly_chart(fig, use_container_width=True)

    # Display data table
    st.dataframe(df)

if __name__ == "__main__":
    main()
