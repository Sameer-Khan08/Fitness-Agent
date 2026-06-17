"""
plan_page.py
------------
Renders the plan page. Shows the user profile summary and triggers
AI plan generation via the fitness agent when the button is clicked.
"""

import streamlit as st

from src.agents.fitness_agent import generate_plan
from src.ui.components import show_medical_disclaimer


def render_plan_page() -> None:
    """
    Display the plan page with profile summary and AI plan generation.
    """
    st.title("🏋️ TrainWise AI")
    st.subheader("Your Fitness Profile")
    st.markdown("---")

    profile = st.session_state.get("profile")

    if not profile:
        st.error("No profile found. Please complete the onboarding form first.")
        if st.button("← Back to Onboarding"):
            st.session_state.stage = "onboarding"
            st.rerun()
        return

    # ── Profile Summary ──────────────────────────────────────────────────────
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Age", f"{profile.get('age')} yrs")
        st.metric("Height", f"{profile.get('height_cm')} cm")
        st.metric("Weight", f"{profile.get('weight_kg')} kg")

    with col2:
        st.metric("Goal", profile.get("main_goal", "—"))
        st.metric("Fitness Level", profile.get("fitness_level", "—"))
        st.metric("Gender", profile.get("gender", "—"))

    with col3:
        st.metric("Training Days", f"{profile.get('training_days_per_week')} / week")
        st.metric("Session Duration", profile.get("session_duration", "—"))

    st.markdown("---")

    sport = profile.get("sport", "").strip()
    if sport:
        st.info(f"🏅 **Sport:** {sport}")

    injuries = profile.get("injuries", "").strip()
    pain_rating = profile.get("pain_rating", 0)
    if injuries:
        colour = "🟡" if pain_rating <= 4 else "🟠" if pain_rating <= 7 else "🔴"
        st.warning(
            f"{colour} **Reported pain/injuries:** {injuries} &nbsp;&nbsp;|&nbsp;&nbsp; "
            f"**Pain rating:** {pain_rating}/10"
        )

    show_medical_disclaimer()
    st.markdown("---")

    # ── Generation Button ────────────────────────────────────────────────────
    st.markdown("### 🤖 Generate Your AI Plan")
    st.caption(
        "Our AI coach will analyse your profile and build a personalised, "
        "injury-aware weekly training plan just for you."
    )

    if st.button("⚡ Generate My Plan", use_container_width=True, type="primary"):
        with st.spinner("🧠 Your AI coach is building your plan... this takes about 10 seconds."):
            try:
                plan = generate_plan(profile)
                st.session_state.results = plan
                st.session_state.stage = "results"
                st.rerun()
            except RuntimeError as e:
                st.error(f"❌ API error: {e}")
            except ValueError as e:
                st.error(f"❌ Plan parsing error: {e}")
            except Exception as e:
                st.error(f"❌ Unexpected error: {e}")

    st.markdown("")
    if st.button("← Edit Profile", use_container_width=True):
        st.session_state.stage = "onboarding"
        st.rerun()
