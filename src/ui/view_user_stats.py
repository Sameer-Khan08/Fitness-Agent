import streamlit as st
import pandas as pd
from database.fetch.user_other_history import get_daily_stats
from database.fetch.user_workout_history import get_user_workout_history
from src.ui.components import inject_custom_css

def render_dashboard_page():
    inject_custom_css()
    
    st.markdown(f"<h2>Welcome, {st.session_state.username}!</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color: gray;'>Here is your fitness summary.</p>", unsafe_allow_html=True)
    
    # Fetch stats
    stats = get_daily_stats(st.session_state.user_id, limit=7)
    workouts = get_user_workout_history(st.session_state.user_id)
    
    # 1. Summary Metrics
    st.subheader("Today's Overview")
    col1, col2, col3 = st.columns(3)
    
    latest_stat = stats[0] if stats else {'steps': 0, 'active_minutes': 0, 'calories_burned': 0}
    
    with col1:
        st.metric("Steps", f"{latest_stat.get('steps', 0)}")
    with col2:
        st.metric("Active Mins", f"{latest_stat.get('active_minutes', 0)}")
    with col3:
        st.metric("Calories", f"{latest_stat.get('calories_burned', 0)}")
        
    st.markdown("---")
    
    # 2. Progress Tracking (Charts)
    st.subheader("Progress Tracking")
    if stats:
        df_stats = pd.DataFrame(stats)
        df_stats['date'] = pd.to_datetime(df_stats['date'])
        df_stats = df_stats.sort_values('date')
        
        tab_steps, tab_cals = st.tabs(["Steps over time", "Calories over time"])
        with tab_steps:
            st.line_chart(df_stats.set_index('date')['steps'])
        with tab_cals:
            st.line_chart(df_stats.set_index('date')['calories_burned'])
    else:
        st.info("No daily stats recorded yet. Start logging to see your progress!")
        
    st.markdown("---")
    
    # 3. Activity Log
    st.subheader("Activity Log")
    if workouts:
        for w in workouts:
            st.markdown(f"**{w['date']}** - {w['duration_minutes']} mins, {w['calories_burned']} cals")
            if w['notes']:
                st.markdown(f"> *{w['notes']}*")
    else:
        st.info("No workout history found.")
        
    st.markdown("---")
    
    # Actions
    st.subheader("Actions")
    colA, colB = st.columns(2)
    with colA:
        if st.button("Generate New Workout Plan", use_container_width=True):
            st.session_state.stage = "onboarding"
            st.rerun()
    with colB:
        if st.button("Logout", use_container_width=True):
            st.session_state.clear()
            st.session_state.stage = "auth"
            st.rerun()
