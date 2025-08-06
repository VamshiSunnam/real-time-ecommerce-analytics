import streamlit as st
import pandas as pd
import json
import time
from streamlit_autorefresh import st_autorefresh
import plotly.express as px
from datetime import datetime
import os

st.set_page_config(
    page_title="Real-time E-commerce Analytics", 
    page_icon="📊",
    layout="wide"
)

def read_events_from_file(filepath="data/live_events.json", max_lines=1000):
    """Read recent events from file"""
    if not os.path.exists(filepath):
        return []
    
    try:
        with open(filepath, "r") as f:
            lines = f.readlines()
            # Get last max_lines
            recent_lines = lines[-max_lines:] if len(lines) > max_lines else lines
            events = [json.loads(line.strip()) for line in recent_lines if line.strip()]
            return events
    except Exception as e:
        st.error(f"Error reading events: {e}")
        return []

def process_events(events):
    """Process events into aggregated data"""
    if not events:
        return pd.DataFrame(), pd.DataFrame()
    
    df = pd.DataFrame(events)
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    
    # Events by type
    events_summary = df['event_type'].value_counts().reset_index()
    events_summary.columns = ['event_type', 'event_count']
    
    # Revenue data (purchases only)
    purchases = df[df['event_type'] == 'purchase'].copy()
    if not purchases.empty:
        purchases['minute'] = purchases['timestamp'].dt.floor('T')
        revenue_summary = purchases.groupby('minute').agg({
            'total_amount': ['sum', 'mean', 'count']
        }).reset_index()
        revenue_summary.columns = ['window_start', 'total_revenue', 'avg_order_value', 'purchase_count']
    else:
        revenue_summary = pd.DataFrame()
    
    return events_summary, revenue_summary

def main():
    st.title("🚀 Real-time E-commerce Analytics Dashboard")
    st.markdown("Live streaming analytics powered by File-based streaming + Streamlit")
    
    # Auto-refresh every 3 seconds
    count = st_autorefresh(interval=3000, limit=2000, key="dashboard_refresh")
    
    st.markdown(f"🔄 Refreshed: {count} times | Last update: {time.strftime('%H:%M:%S')}")
    
    # Read events
    events = read_events_from_file()
    events_df, revenue_df = process_events(events)
    
    if not events:
        st.warning("No events found. Make sure the producer is running!")
        st.info("Run: `cd producers && python simple_file_producer.py`")
        return
    
    # KPIs
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if not revenue_df.empty:
            total_revenue = revenue_df['total_revenue'].sum()
            st.metric("💰 Total Revenue", f"${total_revenue:.2f}")
        else:
            st.metric("💰 Total Revenue", "$0.00")
    
    with col2:
        if not revenue_df.empty:
            avg_order = revenue_df['avg_order_value'].mean()
            st.metric("🛒 Avg Order", f"${avg_order:.2f}")
        else:
            st.metric("🛒 Avg Order", "$0.00")
    
    with col3:
        total_events = len(events)
        st.metric("📊 Total Events", f"{total_events:,}")
    
    with col4:
        if not events_df.empty:
            page_views = events_df[events_df['event_type'] == 'page_view']['event_count'].iloc[0] if 'page_view' in events_df['event_type'].values else 0
            purchases = events_df[events_df['event_type'] == 'purchase']['event_count'].iloc[0] if 'purchase' in events_df['event_type'].values else 0
            conversion = (purchases / page_views * 100) if page_views > 0 else 0
            st.metric("🎯 Conversion", f"{conversion:.1f}%")
        else:
            st.metric("🎯 Conversion", "0%")
    
    # Charts
    col1, col2 = st.columns([2, 1])
    
    with col1:
        if not revenue_df.empty:
            fig = px.line(revenue_df, x='window_start', y='total_revenue', 
                         title="Revenue Over Time", markers=True)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No revenue data yet")
    
    with col2:
        if not events_df.empty:
            fig = px.pie(events_df, values='event_count', names='event_type',
                        title="Event Distribution")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No events data yet")
    
    # Recent events
    st.markdown("## 📋 Recent Events")
    recent_events = events[-10:] if len(events) > 10 else events
    df_display = pd.DataFrame(recent_events)[['event_type', 'product_name', 'total_amount', 'timestamp']]
    st.dataframe(df_display, use_container_width=True)

if __name__ == "__main__":
    main()