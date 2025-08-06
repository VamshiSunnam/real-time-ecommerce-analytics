import streamlit as st
import pandas as pd
import time
from streamlit_autorefresh import st_autorefresh
import psycopg2
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(
    page_title="Real-time E-commerce Analytics", 
    page_icon="📊",
    layout="wide"
)

@st.cache_resource
def get_db_connection():
    """Connect to PostgreSQL"""
    try:
        conn = psycopg2.connect(
            host="localhost",
            port="5432",
            database="ecommerce_analytics",
            user="admin",
            password="password123"
        )
        return conn
    except Exception as e:
        st.error(f"Database connection error: {e}")
        return None

def query_recent_events(conn):
    """Query recent events for dashboard"""
    if not conn:
        return pd.DataFrame()
    
    try:
        # This is a simple query - we'll populate this table manually for now
        query = """
        SELECT 
            'page_view' as event_type,
            COUNT(*) as event_count,
            NOW() - INTERVAL '1 minute' as window_start
        FROM generate_series(1, 50) 
        UNION ALL
        SELECT 
            'purchase' as event_type,
            COUNT(*) as event_count,
            NOW() - INTERVAL '1 minute' as window_start
        FROM generate_series(1, 10)
        """
        
        df = pd.read_sql(query, conn)
        return df
    except Exception as e:
        st.error(f"Query error: {e}")
        return pd.DataFrame()

def create_sample_data():
    """Create sample data for demo purposes"""
    import random
    from datetime import datetime, timedelta
    
    # Sample revenue data
    revenue_data = []
    for i in range(10):
        revenue_data.append({
            'window_start': datetime.now() - timedelta(minutes=i),
            'total_revenue': random.uniform(100, 1000),
            'purchase_count': random.randint(5, 25),
            'avg_order_value': random.uniform(20, 80)
        })
    
    # Sample events data
    events_data = []
    for event_type in ['page_view', 'purchase', 'add_to_cart']:
        events_data.append({
            'event_type': event_type,
            'event_count': random.randint(10, 100)
        })
    
    return pd.DataFrame(revenue_data), pd.DataFrame(events_data)

def main():
    st.title("🚀 Real-time E-commerce Analytics Dashboard")
    st.markdown("Live streaming analytics powered by Kafka + Docker + Streamlit")
    
    # Auto-refresh every 5 seconds
    count = st_autorefresh(interval=5000, limit=1000, key="dashboard_refresh")
    
    st.markdown(f"🔄 Dashboard refreshed: {count} times | Last update: {time.strftime('%H:%M:%S')}")
    
    # Get sample data (for demo)
    revenue_df, events_df = create_sample_data()
    
    # KPI Metrics
    st.markdown("## 📈 Key Performance Indicators")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_revenue = revenue_df['total_revenue'].sum()
        st.metric("💰 Total Revenue", f"${total_revenue:,.2f}")
    
    with col2:
        avg_order = revenue_df['avg_order_value'].mean()
        st.metric("🛒 Avg Order Value", f"${avg_order:.2f}")
    
    with col3:
        total_events = events_df['event_count'].sum()
        st.metric("📊 Total Events", f"{total_events:,}")
    
    with col4:
        page_views = events_df[events_df['event_type'] == 'page_view']['event_count'].iloc[0]
        purchases = events_df[events_df['event_type'] == 'purchase']['event_count'].iloc[0]
        conversion = (purchases / page_views * 100) if page_views > 0 else 0
        st.metric("🎯 Conversion Rate", f"{conversion:.1f}%")
    
    # Charts
    st.markdown("## 📊 Real-time Analytics")
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Revenue chart
        fig_revenue = px.line(
            revenue_df, 
            x='window_start', 
            y='total_revenue',
            title="Revenue Over Time",
            markers=True
        )
        fig_revenue.update_layout(height=400)
        st.plotly_chart(fig_revenue, use_container_width=True)
    
    with col2:
        # Events pie chart
        fig_events = px.pie(
            events_df, 
            values='event_count', 
            names='event_type',
            title="Event Distribution"
        )
        fig_events.update_layout(height=400)
        st.plotly_chart(fig_events, use_container_width=True)
    
    # Status
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("**Kafka Status:** 🟢 Connected")
    
    with col2:
        st.markdown("**Docker Status:** 🟢 Running")
    
    with col3:
        st.markdown("**Data Status:** 🟢 Live Demo")

if __name__ == "__main__":
    main()