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
)


def render_results_page() -> None:
    """
    Display the results page using the premium dark athletic theme.
    """
    # 1. Inject Custom CSS
    inject_custom_css()

    st.title("Your TrainWise Plan")
    st.subheader("Built from your goal, sport, fitness level, and injury context.")
    st.markdown("---")

    plan = st.session_state.get("results")
    profile = st.session_state.get("profile")

    if not plan or not isinstance(plan, dict) or not profile:
        st.warning("No plan found. Please generate a plan first.")
        if st.button("← Back to Plan Page", width="stretch"):
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
    elif safety_status == "yellow":
        st.warning(f"🟡 **Modify Training:** {safety_summary}")
    else:  # red
        st.error(f"🔴 **Training Capped:** {safety_summary}")

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

    # Section 1: Reality Check
    section_header("Reality Check", "Physiological screening details and recommendations.")
    if recommendations:
        st.markdown("**Recommendations:**")
        for rec in recommendations:
            st.info(f"👉 {rec}")
    else:
        st.caption("No specific recommendations found.")

    # Section 2: Goal Priorities
    section_header("Goal Priorities", "Core focus areas matching your goal.")
    priorities = goal_priorities.get("priorities", [])
    if priorities:
        tags_html = ""
        for item in priorities:
            tags_html += f'<span class="status-badge badge-ready" style="margin-right: 8px; font-size: 11px;">{item.upper()}</span>'
        st.markdown(tags_html, unsafe_allow_html=True)
        st.caption(f"Training Style: **{goal_priorities.get('training_style', 'Balanced').title()}**")
    else:
        st.caption("No specific goal priorities mapped.")

    # Section 3: Sport Demands
    section_header("Sport Demands", "Requisite physical capacities and prehab requirements.")
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

    # Section 4: What to Avoid
    section_header("What to Avoid", "Exercises or patterns restricted to protect joints and tissues.")
    if avoid_list:
        for item in avoid_list:
            st.markdown(
                f"""
                <div class="warning-card">
                    <strong style="color: #FF4B4B;">⚠️ Restricted Pattern:</strong> Avoid {item}
                </div>
                """,
                unsafe_allow_html=True
            )
    else:
        st.markdown(
            """
            <div class="info-card">
                🟢 No major movement restrictions detected.
            </div>
            """,
            unsafe_allow_html=True
        )

    # Section 5: Weekly Plan
    section_header("Weekly Plan", "Click the expander on any exercise to view the technique cues and personalized coach notes.")
    if weekly_schedule:
        for i, day_plan in enumerate(weekly_schedule):
            workout_day_card(day_plan, day_idx=i)
    else:
        st.warning("No weekly plan generated.")

    # Section 6: Coach Notes
    section_header("Coach Notes", "General advice for nutrition, recovery, and program progression.")
    if notes:
        for note in notes:
            st.markdown(
                f"""
                <div class="info-card">
                    💡 <strong>Coach Tip:</strong> {note}
                </div>
                """,
                unsafe_allow_html=True
            )
    else:
        st.caption("No coach notes provided.")

    st.markdown("<br>", unsafe_allow_html=True)
    show_medical_disclaimer()
    st.markdown("---")

    # Buttons
    btn_col1, btn_col2 = st.columns(2)
    with btn_col1:
        if st.button("Back to Profile", width="stretch"):
            st.session_state.stage = "plan"
            st.rerun()

    with btn_col2:
        if st.button("Start Over", width="stretch", type="primary"):
            st.session_state.stage = "onboarding"
            st.session_state.profile = None
            st.session_state.results = []
            st.session_state.image_cache = {}
            st.rerun()
