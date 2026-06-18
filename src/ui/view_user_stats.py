import streamlit as st
import pandas as pd
from src.ui.components import inject_custom_css, section_header, workout_day_card, show_medical_disclaimer, render_page_header
from src.memory.plan_store import get_saved_plans_local

def render_dashboard_page():
    inject_custom_css()
    
    username = st.session_state.get("username") or "Athlete"
    render_page_header(f"Welcome, {username}!", "Track your training statistics and view your saved athletic plans.")
    
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
    st.subheader("Saved Plans")
    
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
        
        if saved_plans:
            if st.button("🗑️ Clear Saved Plans", key="clear_all_saved_plans", type="secondary", use_container_width=True):
                from src.memory.plan_store import clear_saved_plans_local
                clear_saved_plans_local()
                st.toast("🧼 Saved plans cleared successfully!", icon="🗑️")
                st.rerun()
            st.markdown("<br>", unsafe_allow_html=True)
            
        if not saved_plans:
            st.markdown(
                """
                <div class="info-card" style="border-left: 5px solid #60EFFF; padding: 20px; border-radius: 8px;">
                    <h4 style="color: #60EFFF; margin-top: 0; margin-bottom: 8px;">📊 No Saved Plans Found</h4>
                    <p style="margin: 0; font-size: 14px; color: #E0E0E0; line-height: 1.5;">
                        Once you generate a fitness plan, you can click "Save Plan" to archive it here for future reference and comparison.
                    </p>
                </div>
                <br>
                """,
                unsafe_allow_html=True
            )
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

    # Deployment Checklist
    st.markdown("---")
    st.subheader("📋 Deployment Checklist")
    with st.expander("System Deployment Status & Verification Checklist", expanded=False):
        import os
        from src.config.settings import OPENAI_API_KEY, TOGETHER_API_KEY, SUPABASE_URL, SUPABASE_KEY
        
        # 1. Project Files Check
        req_exists = os.path.exists("requirements.txt")
        env_ex_exists = os.path.exists(".env.example")
        readme_exists = os.path.exists("README.md")
        
        st.markdown("**1. Required Deployment Files:**")
        if req_exists:
            st.markdown("✅ `requirements.txt` file exists.")
        else:
            st.markdown("❌ `requirements.txt` file is missing!")
            
        if env_ex_exists:
            st.markdown("✅ `.env.example` file exists.")
        else:
            st.markdown("❌ `.env.example` file is missing!")
            
        if readme_exists:
            st.markdown("✅ `README.md` file exists.")
        else:
            st.markdown("❌ `README.md` file is missing!")
            
        st.markdown("**2. Core Execution Engine:**")
        st.markdown("🟢 **Active**: API Keys are not required for the core rule-based fitness planner.")
        
        st.markdown("**3. External Services Connections:**")
        if OPENAI_API_KEY:
            st.markdown("🟢 **OpenAI key**: Configured (AI Coach explanations enabled)")
        else:
            st.markdown("🟡 **OpenAI key**: Missing (AI Coach explanations disabled)")
            
        if TOGETHER_API_KEY:
            st.markdown("🟢 **Together AI key**: Configured (exercise demo images enabled)")
        else:
            st.markdown("🟡 **Together AI key**: Missing (exercise demo images disabled)")
            
        if SUPABASE_URL and SUPABASE_KEY:
            st.markdown("🟢 **Supabase client**: Configured (cloud database & sync active)")
        else:
            st.markdown("🔵 **Supabase client**: Missing (running in local fallback memory mode)")

    st.markdown("<br>", unsafe_allow_html=True)
    show_medical_disclaimer()
