import streamlit as st
from database.save_new_user import create_user
from database.fetch.user_data import get_user_by_username
from src.ui.components import inject_custom_css

def render_auth_page():
    inject_custom_css()
    
    st.markdown("<h1 style='text-align: center;'>TrainWise AI</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: gray;'>Your Personal Athletic Dashboard</p>", unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["Login", "Sign Up"])
    
    with tab1:
        st.subheader("Welcome Back")
        login_username = st.text_input("Username", key="login_user")
        if st.button("Login", use_container_width=True):
            if login_username:
                user = get_user_by_username(login_username)
                if user:
                    st.session_state.user_id = user['id']
                    st.session_state.username = user['username']
                    st.session_state.stage = "dashboard"
                    st.rerun()
                else:
                    st.error("User not found. Please sign up.")
            else:
                st.warning("Please enter a username.")
                
    with tab2:
        st.subheader("Create an Account")
        signup_username = st.text_input("Username", key="signup_user")
        if st.button("Sign Up", use_container_width=True):
            if signup_username:
                user_id = create_user(signup_username)
                st.session_state.user_id = user_id
                st.session_state.username = signup_username
                st.session_state.stage = "onboarding"  # Go to onboarding for new users
                st.rerun()
            else:
                st.warning("Please enter a username.")
