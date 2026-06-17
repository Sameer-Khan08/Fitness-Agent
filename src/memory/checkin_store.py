"""
checkin_store.py
----------------
Handles saving and retrieving daily check-ins locally in session state.
"""

import streamlit as st
import datetime

def save_checkin_local(checkin: dict) -> None:
    """Save a check-in to the local session state."""
    if "checkins" not in st.session_state:
        st.session_state.checkins = []
        
    checkin_with_meta = checkin.copy()
    checkin_with_meta["timestamp"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    st.session_state.checkins.append(checkin_with_meta)

def get_checkins_local() -> list[dict]:
    """Retrieve all check-ins from the local session state."""
    return st.session_state.get("checkins", [])

def clear_checkins_local() -> None:
    """Clear all check-ins from local session state."""
    st.session_state.checkins = []
