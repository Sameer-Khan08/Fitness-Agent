"""
app.py
------
Main entry point for the TrainWise AI Streamlit application.
Handles page configuration, session state initialisation, and
routing between the onboarding, plan, and results stages.

Run with:
    streamlit run app.py
"""

import streamlit as st

# Import the three UI page rendering functions.
from src.ui.onboarding_page import render_onboarding_page
from src.ui.plan_page import render_plan_page
from src.ui.results_page import render_results_page

# --- Page configuration ---
st.set_page_config(
    page_title="TrainWise AI",
    page_icon="🏋️",
    layout="centered",
)

# --- Session state initialisation ---
# These keys are set once on first load and preserved across reruns.

from src.config.settings import SUPABASE_URL, SUPABASE_KEY
supabase_configured = bool(SUPABASE_URL and SUPABASE_KEY)

if "user_id" not in st.session_state:
    st.session_state.user_id = None

if "username" not in st.session_state:
    st.session_state.username = None

if "stage" not in st.session_state:
    if supabase_configured:
        st.session_state.stage = "auth"
    else:
        st.session_state.stage = "onboarding"

if "profile" not in st.session_state:
    st.session_state.profile = None

if "results" not in st.session_state:
    st.session_state.results = []

if "error" not in st.session_state:
    st.session_state.error = None

if "last_generated_plan" not in st.session_state:
    st.session_state.last_generated_plan = None

# --- Stage-based routing ---
from src.ui.login import render_auth_page
from src.ui.view_user_stats import render_dashboard_page

current_stage = st.session_state.stage

if not supabase_configured and current_stage in ["auth", "dashboard"]:
    st.session_state.stage = "onboarding"
    current_stage = "onboarding"

if current_stage == "auth":
    render_auth_page()

elif current_stage == "dashboard":
    render_dashboard_page()

elif current_stage == "onboarding":
    render_onboarding_page()

elif current_stage == "plan":
    render_plan_page()

elif current_stage == "results":
    render_results_page()

else:
    # Unknown stage — reset to auth as a safe fallback.
    st.session_state.stage = "auth"
    st.rerun()
