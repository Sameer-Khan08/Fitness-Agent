"""
plan_store.py
-------------
Handles saving and retrieving generated training plans.
Supports local session state storage.
"""

import streamlit as st
import datetime

def save_plan_local(plan: dict) -> None:
    """Save a plan to the local session state."""
    if "saved_plans" not in st.session_state:
        st.session_state.saved_plans = []
        
    # Add a timestamp to the plan if it doesn't have one
    plan_with_meta = plan.copy()
    plan_with_meta["saved_at"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    st.session_state.saved_plans.append(plan_with_meta)

def get_saved_plans_local() -> list[dict]:
    """Retrieve all plans from the local session state."""
    return st.session_state.get("saved_plans", [])

def clear_saved_plans_local() -> None:
    """Clear all saved plans from local session state."""
    st.session_state.saved_plans = []
