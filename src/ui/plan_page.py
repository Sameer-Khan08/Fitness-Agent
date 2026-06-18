"""
plan_page.py
------------
Renders the plan confirmation page. Displays the athlete profile summary,
dashboard metrics, checks to perform, and triggers the AI generator.
"""

import streamlit as st
from src.agents.fitness_agent import generate_plan as generate_fitness_plan
from src.ui.components import (
    inject_custom_css,
    section_header,
    metric_card,
    profile_card,
    show_medical_disclaimer,
    render_page_header,
)


def render_plan_page() -> None:
    """
    Display the confirmation and planning dashboard page.
    """
    # 1. Custom CSS
    inject_custom_css()

    render_page_header("Current Plan", "Generate and customize your athletic training program.")

    profile = st.session_state.get("profile")

    if not profile:
        st.markdown(
            """
            <div class="warning-card" style="border-left: 5px solid #FFD700; padding: 20px; border-radius: 8px;">
                <h4 style="color: #FFD700; margin-top: 0; margin-bottom: 8px;">📋 Profile Missing</h4>
                <p style="margin: 0; font-size: 14px; color: #E0E0E0; line-height: 1.5;">
                    To build and view your customized training plan, we first need to understand your fitness level, goals, and safety constraints.
                </p>
            </div>
            <br>
            """,
            unsafe_allow_html=True
        )
        if st.button("Set Up Profile", type="primary", use_container_width=True):
            st.session_state.stage = "onboarding"
            st.rerun()
        return

    # 2. Section Header: Your Training Profile
    section_header("Your Training Profile", "Review your submitted details before plan generation.")

    # 3. Profile Card
    profile_card(profile)

    # 4. 3 Metric Cards
    col_m1, col_m2, col_m3 = st.columns(3)
    with col_m1:
        metric_card(label="Goal Focus", value=profile.get("main_goal", "—"))
    with col_m2:
        metric_card(label="Sport Demand", value=profile.get("sport", "—"))
    with col_m3:
        pain_val = profile.get("pain_rating", 0)
        metric_card(label="Current Pain", value=f"{pain_val}/10", helper="Active check enabled" if pain_val > 0 else "Clear")

    st.markdown("<br>", unsafe_allow_html=True)

    # 5. Section: What TrainWise will check
    section_header("What TrainWise will check", "The coaching engine will evaluate the following parameters to ensure performance and safety.")

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(
            """
            <div class="metric-card" style="height: 140px; display: flex; flex-direction: column; justify-content: center; align-items: center;">
                <span style="font-size: 1.5rem; margin-bottom: 5px;">🎯</span>
                <h6 style="margin: 0 0 4px 0; color: white;">Training Goal</h6>
                <p style="font-size: 11px; color: #8C96A8; margin: 0; line-height: 1.3;">Selects ideal rep ranges, rest, volume, and target load focus.</p>
            </div>
            """,
            unsafe_allow_html=True
        )
    with col2:
        st.markdown(
            """
            <div class="metric-card" style="height: 140px; display: flex; flex-direction: column; justify-content: center; align-items: center;">
                <span style="font-size: 1.5rem; margin-bottom: 5px;">🏅</span>
                <h6 style="margin: 0 0 4px 0; color: white;">Sport Demands</h6>
                <p style="font-size: 11px; color: #8C96A8; margin: 0; line-height: 1.3;">Incorporate patterns, conditioning, and prehab matching your sport.</p>
            </div>
            """,
            unsafe_allow_html=True
        )
    with col3:
        st.markdown(
            """
            <div class="metric-card" style="height: 140px; display: flex; flex-direction: column; justify-content: center; align-items: center;">
                <span style="font-size: 1.5rem; margin-bottom: 5px;">⚡</span>
                <h6 style="margin: 0 0 4px 0; color: white;">Fitness Level</h6>
                <p style="font-size: 11px; color: #8C96A8; margin: 0; line-height: 1.3;">Adapts exercise complexity and progression rates to your experience.</p>
            </div>
            """,
            unsafe_allow_html=True
        )
    with col4:
        st.markdown(
            """
            <div class="metric-card" style="height: 140px; display: flex; flex-direction: column; justify-content: center; align-items: center;">
                <span style="font-size: 1.5rem; margin-bottom: 5px;">🛡️</span>
                <h6 style="margin: 0 0 4px 0; color: white;">Pain/Injury Risk</h6>
                <p style="font-size: 11px; color: #8C96A8; margin: 0; line-height: 1.3;">Screens flags, flags pain ratings, and builds safe movement boundaries.</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown("<br>", unsafe_allow_html=True)
    show_medical_disclaimer()
    st.markdown("<hr style='margin:20px 0; opacity:0.1;'>", unsafe_allow_html=True)

    # 6. Action buttons
    if st.button("Generate My Training Plan", width="stretch", type="primary"):
        with st.spinner("🧠 TrainWise coaching engine is processing your profile..."):
            try:
                plan = generate_fitness_plan(profile)
                st.session_state.results = plan
                st.session_state.ai_explanation = None
                st.session_state.stage = "results"
                st.rerun()
            except Exception as e:
                st.error(f"❌ Generation failed: {e}")

    st.markdown("")
    if st.button("Edit Profile", width="stretch"):
        st.session_state.stage = "onboarding"
        st.rerun()
