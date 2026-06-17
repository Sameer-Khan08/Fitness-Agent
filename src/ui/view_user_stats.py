import streamlit as st
import pandas as pd
from src.ui.components import inject_custom_css
from src.memory.plan_store import get_saved_plans_local
from src.ui.components import section_header, workout_day_card

def render_dashboard_page():
    inject_custom_css()
    
    username = st.session_state.get("username") or "Athlete"
    st.markdown(f"<h2>Welcome, {username}!</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color: gray;'>Here is your fitness dashboard.</p>", unsafe_allow_html=True)
    
    # 1. Fetch stats (try/except for local mode without DB)
    stats = []
    workouts = []
    try:
        from database.fetch.user_other_history import get_daily_stats
        from database.fetch.user_workout_history import get_user_workout_history
        if st.session_state.get("user_id"):
            stats = get_daily_stats(st.session_state.user_id, limit=7)
            workouts = get_user_workout_history(st.session_state.user_id)
    except Exception:
        pass
    
    # Show existing stats if they exist
    if stats or workouts:
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
            st.info("No daily stats recorded yet.")
            
        st.markdown("---")
    
    # 2. Saved Plans History
    st.subheader("Saved Training Plans")
    
    # Let's see if a plan is currently selected for viewing
    selected_plan = st.session_state.get("selected_saved_plan")
    
    if selected_plan:
        if st.button("← Back to Dashboard"):
            st.session_state.selected_saved_plan = None
            st.rerun()
            
        st.markdown(f"### Saved Plan: {selected_plan.get('saved_at', 'Unknown Date')}")
        
        # Show safety and goals
        safety = selected_plan.get("safety", {})
        st.info(f"**Safety Status:** {safety.get('status', 'Unknown')} - {safety.get('summary', '')}")
        
        goal_priorities = selected_plan.get("goal_priorities", {})
        priorities = goal_priorities.get("priorities", [])
        if priorities:
            st.write(f"**Goal Priorities:** {', '.join(priorities)}")
            
        sport_demands = selected_plan.get("sport_demands", {})
        demands = sport_demands.get("demands", [])
        if demands:
            st.write(f"**Sport Demands:** {', '.join(demands)}")
            
        weekly_schedule = selected_plan.get("weekly_plan", [])
        if weekly_schedule:
            for i, day_plan in enumerate(weekly_schedule):
                workout_day_card(day_plan, day_idx=i)
        else:
            st.warning("No weekly schedule found in this saved plan.")
            
        st.markdown("---")
    else:
        # Show list of saved plans
        saved_plans = get_saved_plans_local()
        st.caption(f"Total saved plans: {len(saved_plans)}")
        
        if not saved_plans:
            st.info("You haven't saved any training plans yet.")
        else:
            for idx, plan in enumerate(saved_plans):
                date_saved = plan.get("saved_at", "Unknown Date")
                profile_summary = plan.get("profile_summary", {})
                goal = profile_summary.get("main_goal", "General")
                sport = profile_summary.get("sport", "None")
                safety = plan.get("safety", {}).get("status", "Unknown")
                
                with st.container():
                    st.markdown(f"**{date_saved}** | Goal: {goal} | Sport: {sport} | Safety: {safety.capitalize()}")
                    if st.button("View Details", key=f"view_plan_{idx}"):
                        st.session_state.selected_saved_plan = plan
                        st.rerun()
                    st.markdown("---")
    
    # Actions
    st.subheader("Actions")
    colA, colB = st.columns(2)
    with colA:
        if st.button("Generate New Workout Plan", use_container_width=True):
            st.session_state.stage = "onboarding"
            st.rerun()
    with colB:
        # Only show logout if user has an active session/username
        if st.session_state.get("username"):
            if st.button("Logout", use_container_width=True):
                st.session_state.clear()
                st.session_state.stage = "auth"
                st.rerun()
