import sys
import os
import streamlit as st

# Add project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from dashboard.auth import login, is_authenticated, logout
import config

st.set_page_config(
    page_title=config.DASHBOARD_TITLE,
    page_icon="🛍️",
    layout="wide",
    initial_sidebar_state="expanded"
)

def main():
    """Main function to run the Streamlit dashboard."""
    if not is_authenticated():
        login()
        return

    st.sidebar.title(f"Welcome, {st.session_state['username']}!")
    logout()

    st.title("Welcome to the Real-time Ecommerce Dashboard!")
    st.write("Select a page from the sidebar to view detailed analytics.")

if __name__ == "__main__":
    main()
