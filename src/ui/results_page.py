"""
results_page.py
---------------
Renders the results page as a structured, visual coaching dashboard.
Pulls directly from local rule-based MVP generator structures.
"""

import streamlit as st
from src.ui.components import (
    inject_custom_css,
    section_header,
    safety_card,
    workout_day_card,
    render_status_badge,
    show_medical_disclaimer,
    render_page_header,
)


def render_results_page() -> None:
    """
    Display the results page using the premium dark athletic theme.
    """
    # 1. Inject Custom CSS
    inject_custom_css()

    render_page_header("Current Plan", "Your customized training plan designed from your goals, sport, and physiological screening.")

    plan = st.session_state.get("results")
    profile = st.session_state.get("profile")

    if not plan or not isinstance(plan, dict) or not profile:
        st.markdown(
            """
            <div class="warning-card" style="border-left: 5px solid #FFD700; padding: 20px; border-radius: 8px;">
                <h4 style="color: #FFD700; margin-top: 0; margin-bottom: 8px;">💪 No Active Plan</h4>
                <p style="margin: 0; font-size: 14px; color: #E0E0E0; line-height: 1.5;">
                    You don't have an active training plan yet. If you have already set up your profile, you can generate your plan now.
                </p>
            </div>
            <br>
            """,
            unsafe_allow_html=True
        )
        col_a, col_b = st.columns(2)
        with col_a:
            if st.button("Profile Setup", use_container_width=True):
                st.session_state.stage = "onboarding"
                st.rerun()
        with col_b:
            if st.button("Generate Plan", type="primary", use_container_width=True):
                st.session_state.stage = "plan"
                st.rerun()
        return

    # Extract rule-based MVP elements
    safety = plan.get("safety", {})
    safety_status = safety.get("status", "yellow")
    safety_summary = safety.get("summary", "")
    avoid_list = safety.get("avoid", [])
    recommendations = safety.get("recommendations", [])

    medical = plan.get("medical", {})
    has_red_flags = medical.get("has_red_flags", False)
    red_flag_warnings = medical.get("flags", [])
    medical_message = medical.get("message", "")

    goal_priorities = plan.get("goal_priorities", {})
    sport_demands = plan.get("sport_demands", {})
    weekly_schedule = plan.get("weekly_plan", [])
    notes = plan.get("notes", [])

    # 2. Safety status messaging
    if safety_status == "green":
        st.success(f"🟢 **Safe to Train:** {safety_summary}")
        st.markdown(
            """
            <div class="info-card" style="border-left: 5px solid #00FF87; margin-bottom: 20px;">
                💡 <strong>Safety Recommendation:</strong> Even though you are safe to train normally, 
                always begin sessions with a dynamic warm-up and progress training volume/intensity gradually.
            </div>
            """,
            unsafe_allow_html=True
        )
    elif safety_status == "yellow":
        st.warning(f"🟡 **Modify Training:** {safety_summary}")
        st.markdown(
            """
            <div class="warning-card" style="border-left: 5px solid #FFD700; margin-bottom: 20px;">
                ⚠️ <strong>Safety Recommendation:</strong> Avoid high-risk drills (sprinting, jumping, plyometrics) 
                and any exercise matching your injury areas. Cap intensity at a low-to-moderate level and adjust ranges of motion if pain occurs.
            </div>
            """,
            unsafe_allow_html=True
        )
    else:  # red
        st.error(f"🔴 **Training Capped:** {safety_summary}")
        st.markdown(
            """
            <div class="warning-card" style="border-left: 5px solid #FF4B4B; margin-bottom: 20px;">
                🚨 <strong>CRITICAL SAFETY WARNING:</strong> Your profile indicates high pain or medical red flags. 
                <strong>Do NOT attempt intense training.</strong> Focus only on light recovery, stability, or active rehabilitation, 
                and immediately consult a qualified doctor or physiotherapist for guidance.
            </div>
            """,
            unsafe_allow_html=True
        )

    # 3. Medical warnings
    if has_red_flags:
        st.error(f"🚨 **Medical Alert:** {medical_message}")
        if red_flag_warnings:
            for flag in red_flag_warnings:
                st.error(f"⚠️ {flag}")
        st.markdown("---")

    # 4. Summary metrics
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.markdown("**Status**")
        render_status_badge(safety_status)
    with col2:
        st.markdown("**Goal**")
        st.markdown(f"🎯 **{profile.get('main_goal', '—')}**")
    with col3:
        st.markdown("**Sport**")
        st.markdown(f"🏅 **{profile.get('sport', '—')}**")
    with col4:
        st.markdown("**Days / Wk**")
        st.markdown(f"📅 **{profile.get('training_days_per_week', '—')} Days**")
    with col5:
        st.markdown("**Pain Rating**")
        pain_val = profile.get("pain_rating", 0)
        pain_color = "red" if pain_val >= 7 else "orange" if pain_val > 3 else "green"
        st.markdown(f"🛡️ <strong style='color:{pain_color};'>{pain_val}/10</strong>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── 5. SECTIONS ──────────────────────────────────────────────────────────

    # Section 1: Reality Check (Expander)
    section_header("Reality Check", "Physiological screening details and recommendations.")
    with st.expander("🩺 View Reality Check details", expanded=True):
        if recommendations:
            st.markdown("**Recommendations:**")
            for rec in recommendations:
                st.info(f"👉 {rec}")
        else:
            st.caption("No specific recommendations found.")

        st.markdown("**What to Avoid:**")
        if avoid_list:
            for item in avoid_list:
                st.markdown(
                    f"""
                    <div class="warning-card" style="margin-bottom: 8px;">
                        <strong style="color: #FF4B4B;">⚠️ Restricted Pattern:</strong> Avoid {item}
                    </div>
                    """,
                    unsafe_allow_html=True
                )
        else:
            st.markdown(
                """
                <div class="info-card" style="margin-bottom: 8px;">
                    🟢 No major movement restrictions detected.
                </div>
                """,
                unsafe_allow_html=True
            )

    # Section 2: Goal Priorities (Expander)
    section_header("Goal Priorities", "Core focus areas matching your goal.")
    with st.expander("🎯 View Goal Priorities", expanded=False):
        priorities = goal_priorities.get("priorities", [])
        if priorities:
            tags_html = ""
            for item in priorities:
                tags_html += f'<span class="status-badge badge-ready" style="margin-right: 8px; font-size: 11px;">{item.upper()}</span>'
            st.markdown(tags_html, unsafe_allow_html=True)
            st.caption(f"Training Style: **{goal_priorities.get('training_style', 'Balanced').title()}**")
        else:
            st.caption("No specific goal priorities mapped.")

    # Section 3: Sport Demands (Expander)
    section_header("Sport Demands", "Requisite physical capacities and prehab requirements.")
    with st.expander("🏃 View Sport Demands", expanded=False):
        demands = sport_demands.get("demands", [])
        prehab = sport_demands.get("prehab_focus", [])
        
        col_d1, col_d2 = st.columns(2)
        with col_d1:
            st.markdown("**Sport Capacities:**")
            if demands:
                for dem in demands:
                    st.markdown(f"⚡ {dem.title()}")
            else:
                st.caption("No specific demands defined.")
                
        with col_d2:
            st.markdown("**Prehab Focus Areas:**")
            if prehab:
                for ph in prehab:
                    st.markdown(f"🛡️ {ph.title()}")
            else:
                st.caption("No prehab target zones defined.")

    # Section 4: Weekly Plan (Day tabs)
    st.subheader("Weekly Plan")
    st.caption("Select a day to view the workout.")
    
    if weekly_schedule:
        day_tabs = st.tabs([day_plan.get("day", f"Day {i+1}") for i, day_plan in enumerate(weekly_schedule)])
        for day_idx, tab in enumerate(day_tabs):
            with tab:
                workout_day_card(weekly_schedule[day_idx], day_idx=day_idx)
    else:
        st.info("Generate a plan first to view workout days.")

    # Section 5: Notes & Coach Advice (Expander)
    section_header("Notes", "General advice for nutrition, recovery, and program progression.")
    with st.expander("💡 View Coach Notes & AI Coach Explanation", expanded=False):
        st.markdown("### Coach Tips")
        if notes:
            for note in notes:
                st.markdown(f"- {note}")
        else:
            st.caption("No coach notes provided.")
            
        st.markdown("<hr style='margin:18px 0; opacity:0.1;'>", unsafe_allow_html=True)
        st.markdown("### AI Coach Explanation")
        
        explanation_val = st.session_state.get("ai_explanation")
        if explanation_val:
            st.markdown(
                f"""
                <div class="fitness-card">
                    {explanation_val}
                </div>
                """,
                unsafe_allow_html=True
            )
        else:
            if st.button("🤖 Generate AI Explanation", type="secondary"):
                with st.spinner("Generating explanation..."):
                    from src.agents.fitness_agent import generate_ai_plan_explanation
                    explanation = generate_ai_plan_explanation(plan)
                    st.session_state.ai_explanation = explanation
                    st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)
    show_medical_disclaimer()
    st.markdown("---")

    # Buttons
    if st.button("💾 Save Plan", width="stretch", type="primary"):
        from src.memory.plan_store import save_plan_local
        save_plan_local(plan)
        st.success("✅ Plan saved successfully!")
        st.info("Saved for this session only (local storage).")
        
    st.markdown("<br>", unsafe_allow_html=True)

    if st.button("📊 Daily Check-in / Adjust Today's Workout", width="stretch", type="primary"):
        st.session_state.stage = "checkin"
        st.rerun()
        
    st.markdown("<br>", unsafe_allow_html=True)

    btn_col1, btn_col2 = st.columns(2)
    with btn_col1:
        if st.button("Back to Profile", width="stretch"):
            st.session_state.stage = "plan"
            st.rerun()

    with btn_col2:
        if st.button("Start Over", width="stretch", type="primary"):
            from src.ui.components import reset_session_state
            reset_session_state()
            st.session_state.stage = "onboarding"
            st.rerun()
