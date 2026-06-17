"""
checkin_page.py
---------------
Renders the daily check-in form to assess readiness before training.
"""

import streamlit as st
from src.memory.checkin_store import save_checkin_local
from src.planning.readiness_engine import calculate_readiness
from src.planning.workout_adjuster import adjust_workout_for_readiness
from src.ui.components import inject_custom_css, show_medical_disclaimer

def render_checkin_page() -> None:
    """Display the daily check-in form."""
    inject_custom_css()
    
    st.title("Daily Check-in")
    st.markdown("Let's see how your body is feeling today before you train.")
    
    if st.button("← Cancel", type="secondary"):
        st.session_state.stage = "results"
        st.rerun()
        
    with st.form("daily_checkin_form"):
        st.subheader("Recovery")
        col1, col2 = st.columns(2)
        with col1:
            sleep_quality = st.selectbox("Sleep Quality", ["poor", "okay", "good"], index=1)
            soreness = st.slider("Muscle Soreness (0 = None, 10 = Cannot move)", 0, 10, 0)
        with col2:
            energy_level = st.selectbox("Energy Level", ["low", "medium", "high"], index=1)
            stress = st.slider("Stress Level (0 = None, 10 = Overwhelmed)", 0, 10, 0)
            
        st.subheader("Pain & Symptoms")
        col3, col4 = st.columns(2)
        with col3:
            pain_rating = st.slider("Current Pain Rating (0 = None, 10 = Severe)", 0, 10, 0)
            pain_area = st.text_input("Pain Area Today (if any)", placeholder="e.g. lower back, knee")
        with col4:
            pain_trend = st.selectbox("Pain Trend", ["better", "same", "worse"], index=1)
            
        st.subheader("Context")
        col5, col6 = st.columns(2)
        with col5:
            trained_yesterday = st.radio("Did you train yesterday?", ["yes", "no"], index=1)
        with col6:
            ready_to_train = st.radio("Do you feel ready to train?", ["yes", "no"], index=0)
            
        submitted = st.form_submit_button("Submit Check-in", type="primary", use_container_width=True)
        
        if submitted:
            checkin = {
                "sleep_quality": sleep_quality,
                "energy_level": energy_level,
                "soreness": soreness,
                "stress": stress,
                "pain_rating": pain_rating,
                "pain_area": pain_area,
                "pain_trend": pain_trend,
                "trained_yesterday": trained_yesterday,
                "ready_to_train": ready_to_train
            }
            
            save_checkin_local(checkin)
            
            readiness = calculate_readiness(checkin)
            st.session_state.current_readiness = readiness
            
            # If a current plan exists, grab today's workout and adjust
            plan = st.session_state.get("results")
            if plan and isinstance(plan, dict) and "weekly_plan" in plan and len(plan["weekly_plan"]) > 0:
                # We'll just adjust the first day or current day if we had a tracker.
                # For simplicity, adjust day 0.
                today_workout = plan["weekly_plan"][0]
                adjusted = adjust_workout_for_readiness(today_workout, readiness)
                st.session_state.adjusted_today_workout = adjusted
            else:
                st.session_state.adjusted_today_workout = None
                
            st.session_state.stage = "daily_result"
            st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)
    show_medical_disclaimer()
