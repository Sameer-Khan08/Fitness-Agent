"""
results_page.py
---------------
Renders the results page in a structured, visual coaching dashboard format.
Leverages custom CSS cards, badges, and workout blocks.
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
from src.planning.goal_engine import get_goal_modifiers
from src.planning.sport_engine import get_sport_context


def render_results_page() -> None:
    """
    Display the results page using the premium athletic theme.
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

    # 2. Pre-calculate Safety & Medical attributes
    pain_rating = profile.get("pain_rating", 0)
    red_flag_warnings = plan.get("red_flag_warnings", [])
    injuries = profile.get("injuries", "")

    # Safety status mapping
    if pain_rating >= 8 or red_flag_warnings:
        safety_status = "Red"
        safety_summary = "High pain rating or red flag symptoms detected. Cap intensity, prioritize active rehab, or seek professional medical advice immediately."
    elif pain_rating > 0 or injuries:
        safety_status = "Yellow"
        safety_summary = f"Training must be modified to accommodate: {injuries if injuries else 'reported pain'}. Avoid loading painful patterns."
    else:
        safety_status = "Green"
        safety_summary = "Athlete cleared for standard training progression. Continue monitoring weekly fatigue and range of motion."

    safety_dict = {
        "status": safety_status,
        "summary": safety_summary
    }

    medical_dict = {
        "warnings": red_flag_warnings,
        "message": plan.get("injury_notes", "")
    }

    # 3. Safety Card at the top
    safety_card(safety_dict, medical_dict)

    # 4. Summary columns
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
        pain_color = "red" if pain_rating >= 7 else "orange" if pain_rating > 0 else "green"
        st.markdown(f"🛡️ <strong style='color:{pain_color};'>{pain_rating}/10</strong>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── 5. SECTIONS ──────────────────────────────────────────────────────────

    # Section 1: Reality Check
    section_header("Reality Check", "Status check of physical readiness and symptom levels.")
    if safety_status == "Red":
        st.error("🚨 **CRITICAL WARNING:** High risk of symptom aggravation detected. Do not force movements.")
    st.info(f"🔍 **Problem Diagnosis:** {plan.get('problem_diagnosis', 'No specific diagnosis calculated.')}")
    st.info(f"🎯 **Targeted Solution:** {plan.get('specific_solution', 'No specific solution calculated.')}")

    # Section 2: Goal Priorities
    section_header("Goal Priorities", "Key physiological focuses targeted in this cycle.")
    mods = get_goal_modifiers(profile.get("main_goal"))
    focus_items = [item.strip() for item in mods.get("focus", "").split(",") if item.strip()]
    if focus_items:
        tags_html = ""
        for item in focus_items:
            tags_html += f'<span class="status-badge badge-ready" style="margin-right: 8px; font-size: 11px;">{item.upper()}</span>'
        st.markdown(tags_html, unsafe_allow_html=True)
    else:
        st.caption("No specific goal priorities found.")

    # Section 3: Sport Demands
    section_header("Sport Demands", "Physical demands and injury-preemption priorities matching your sport.")
    sport_ctx = get_sport_context(profile.get("sport"))
    st.write(sport_ctx)
    # Highlight key patterns as badges based on sport context keywords
    demands_tags = []
    sport_ctx_lower = sport_ctx.lower()
    if "sprint" in sport_ctx_lower:
        demands_tags.append("⚡ Repeated Sprint Ability")
    if "plyo" in sport_ctx_lower or "jump" in sport_ctx_lower:
        demands_tags.append("🚀 Vertical/Plyometrics")
    if "lateral" in sport_ctx_lower or "direction" in sport_ctx_lower:
        demands_tags.append("🔄 Lateral Agility")
    if "endurance" in sport_ctx_lower or "aerobic" in sport_ctx_lower:
        demands_tags.append("❤️ Aerobic capacity")
    if "shoulder" in sport_ctx_lower or "rotator" in sport_ctx_lower:
        demands_tags.append("🛡️ Shoulder Cuff prehab")
    if "rotation" in sport_ctx_lower:
        demands_tags.append("🔄 Rotational Power")
    if "hamstring" in sport_ctx_lower or "groin" in sport_ctx_lower:
        demands_tags.append("🩹 Hamstring/Groin prehab")
        
    if demands_tags:
        tags_html = ""
        for tag in demands_tags:
            tags_html += f'<span class="status-badge badge-modify" style="margin-right: 8px; font-size: 11px;">{tag.upper()}</span>'
        st.markdown("<div style='margin-top: 8px;'>" + tags_html + "</div>", unsafe_allow_html=True)

    # Section 4: What to Avoid
    section_header("What to Avoid", "Movement patterns restricted for safety.")
    avoid_list = []
    if mods.get("avoid") and mods.get("avoid").lower() != "nothing specific":
        avoid_list.append(mods.get("avoid"))
    if injuries:
        avoid_list.append(f"Loading or stressing the injured/painful area: '{injuries}' directly.")
        
    if avoid_list:
        for item in avoid_list:
            st.markdown(
                f"""
                <div class="warning-card">
                    <strong style="color: #FF4B4B;">⚠️ Restricted:</strong> {item}
                </div>
                """,
                unsafe_allow_html=True
            )
    else:
        st.markdown(
            """
            <div class="info-card">
                🟢 No major movement restrictions detected for this profile.
            </div>
            """,
            unsafe_allow_html=True
        )

    # Section 5: Weekly Plan
    section_header("Weekly Plan", "Click the expander on any exercise to view the technique cues and personalized coach notes.")
    weekly_schedule = plan.get("weekly_schedule", [])
    if weekly_schedule:
        for i, day_plan in enumerate(weekly_schedule):
            workout_day_card(day_plan, day_idx=i)
    else:
        st.warning("No training schedule generated.")

    # Section 6: Coach Notes
    section_header("Coach Notes", "General advice for nutrition, recovery, and program progression.")
    col_n1, col_n2 = st.columns(2)
    with col_n1:
        nut_tip = plan.get("nutrition_tip", "")
        if nut_tip:
            st.markdown(
                f"""
                <div class="info-card" style="height: 100%;">
                    <strong style="color: #60EFFF;">🥗 Nutrition Tip</strong><br/>
                    <p style="margin-top: 5px; font-size: 13px; line-height: 1.5;">{nut_tip}</p>
                </div>
                """,
                unsafe_allow_html=True
            )
    with col_n2:
        rec_adv = plan.get("recovery_advice", "")
        if rec_adv:
            st.markdown(
                f"""
                <div class="info-card" style="height: 100%;">
                    <strong style="color: #60EFFF;">😴 Recovery Strategy</strong><br/>
                    <p style="margin-top: 5px; font-size: 13px; line-height: 1.5;">{rec_adv}</p>
                </div>
                """,
                unsafe_allow_html=True
            )

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
