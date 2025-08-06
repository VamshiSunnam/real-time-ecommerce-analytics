import streamlit as st
import pandas as pd
from dashboard.auth import is_authenticated, login
from consumers.aggregation_engine import db_pool

def fetch_data():
    """Fetch user activity data from the database"""
    conn = db_pool.getconn()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT user_id, total_events, total_spent, last_activity FROM user_activity ORDER BY last_activity DESC")
            data = cursor.fetchall()
            return pd.DataFrame(data, columns=["User ID", "Total Events", "Total Spent", "Last Activity"])
    finally:
        db_pool.putconn(conn)

def main():
    """Display the user activity page"""
    if not is_authenticated():
        login()
        return

    st.title("User Activity")
    
    df = fetch_data()
    
    if df.empty:
        st.warning("No data available yet. Please wait for events to be processed.")
        return

    # Display data table
    st.dataframe(df)

if __name__ == "__main__":
    main()
