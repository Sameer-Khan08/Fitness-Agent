"""
daily_result_page.py
--------------------
Displays the daily readiness results and the adjusted workout plan.
"""

import streamlit as st
from src.ui.components import inject_custom_css, workout_day_card, render_status_badge, show_medical_disclaimer

def render_daily_result_page() -> None:
    """Display readiness status and adjusted workout."""
    inject_custom_css()
    
    st.title("Daily Check-in")
    st.subheader("Daily Readiness")
    st.markdown("---")
    
    readiness = st.session_state.get("current_readiness")
    if not readiness:
        st.warning("No readiness data found.")
        if st.button("← Back"):
            st.session_state.stage = "results"
            st.rerun()
        return
        
    # Readiness Header
    status = readiness.get("readiness", "green")
    score = readiness.get("score", 100)
    
    col1, col2 = st.columns([1, 3])
    with col1:
        st.metric("Readiness Score", f"{score}/100")
        render_status_badge(status)
    with col2:
        st.markdown(f"**Recommendation:** {readiness.get('recommendation', '')}")
        st.info(readiness.get("summary", ""))
        
    # Details
    avoid = readiness.get("avoid_today", [])
    mods = readiness.get("modifications", [])
    
    if avoid or mods:
        st.subheader("Action Plan")
        c1, c2 = st.columns(2)
        with c1:
            if mods:
                st.markdown("**Modifications:**")
                for m in mods:
                    st.markdown(f"- 🔄 {m}")
        with c2:
            if avoid:
                st.markdown("**Avoid Today:**")
                for a in avoid:
                    st.markdown(f"- 🚫 {a}")
                    
    st.markdown("---")
    
    # Adjusted Workout
    adjusted_workout = st.session_state.get("adjusted_today_workout")
    if adjusted_workout:
        st.subheader("Today's Adjusted Workout")
        workout_day_card(adjusted_workout, day_idx=0)
    else:
        st.info("No workout found to adjust.")
        
    st.markdown("---")
    
    # Buttons
    b1, b2, b3 = st.columns(3)
    with b1:
        if st.button("← Back to Results", use_container_width=True):
            st.session_state.stage = "results"
            st.rerun()
    with b2:
        if st.button("🔄 New Check-in", use_container_width=True):
            st.session_state.stage = "checkin"
            st.rerun()
    with b3:
        if st.button("Start Over", use_container_width=True, type="primary"):
            st.session_state.stage = "onboarding"
            st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)
    show_medical_disclaimer()
