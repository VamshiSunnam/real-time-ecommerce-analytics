import streamlit as st
import hashlib

# In a real app, use a database or a secure secret management service
HASHED_PASSWORDS = {
    "admin": hashlib.sha256("password123".encode()).hexdigest(),
    "viewer": hashlib.sha256("viewer_pass".encode()).hexdigest(),
}

def is_authenticated() -> bool:
    """Check if the user is authenticated"""
    return st.session_state.get("authenticated", False)

def login() -> None:
    """Display login form and handle authentication"""
    st.title("Login")
    
    username = st.text_input("Username", key="login_username")
    password = st.text_input("Password", type="password", key="login_password")
    
    if st.button("Login"):
        if _check_credentials(username, password):
            st.session_state["authenticated"] = True
            st.session_state["username"] = username
            st.rerun()
        else:
            st.error("Invalid username or password")

def logout() -> None:
    """Handle user logout"""
    if st.sidebar.button("Logout"):
        st.session_state["authenticated"] = False
        st.session_state["username"] = None
        st.rerun()

def _check_credentials(username: str, password: str) -> bool:
    """Check if username and password are valid"""
    if not username or not password:
        return False
        
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    return HASHED_PASSWORDS.get(username) == hashed_password
