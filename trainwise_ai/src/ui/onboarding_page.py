"""
onboarding_page.py
------------------
Renders the onboarding form where users enter their fitness profile.
Collected data is stored in st.session_state.profile and the app
moves to the "plan" stage on submission.
"""

import streamlit as st


def render_onboarding_page() -> None:
    """
    Display the onboarding page with a fitness profile form.
    On submission, saves the profile to session state and routes
    the user to the plan stage.
    """
    st.title("🏋️ TrainWise AI")
    st.subheader("AI fitness and athletic performance coach.")
    st.markdown("---")
    st.markdown("### Tell us about yourself")
    st.caption("Fill in the form below so we can tailor your training plan.")

    with st.form(key="onboarding_form"):

        col1, col2 = st.columns(2)

        with col1:
            age = st.number_input(
                "Age (years)",
                min_value=12,
                max_value=100,
                value=25,
                step=1,
            )
            height = st.number_input(
                "Height (cm)",
                min_value=100,
                max_value=250,
                value=170,
                step=1,
            )
            gender = st.selectbox(
                "Gender",
                options=["Male", "Female", "Non-binary", "Prefer not to say"],
            )

        with col2:
            weight = st.number_input(
                "Weight (kg)",
                min_value=30,
                max_value=300,
                value=70,
                step=1,
            )
            fitness_level = st.selectbox(
                "Current fitness level",
                options=["Beginner", "Intermediate", "Advanced", "Athlete"],
            )
            training_days = st.slider(
                "Training days per week",
                min_value=1,
                max_value=7,
                value=3,
            )

        main_goal = st.selectbox(
            "Main goal",
            options=[
                "Weight loss",
                "General fitness",
                "Muscle gain",
                "Athletic development",
                "Sport-specific training",
                "Injury rehabilitation",
                "Improve endurance",
            ],
        )

        sport = st.text_input(
            "Sport (if applicable)",
            placeholder="e.g. Football, Swimming, Tennis — leave blank if not applicable",
        )

        session_duration = st.selectbox(
            "Preferred session duration",
            options=["30 minutes", "45 minutes", "60 minutes", "75 minutes", "90+ minutes"],
        )

        injuries = st.text_area(
            "Injuries or pain areas",
            placeholder="e.g. Left knee pain, lower back stiffness — leave blank if none",
            height=80,
        )

        pain_rating = st.slider(
            "Current pain rating (0 = no pain, 10 = severe)",
            min_value=0,
            max_value=10,
            value=0,
        )

        submitted = st.form_submit_button("Build My Plan →", use_container_width=True)

    if submitted:
        # Save the collected profile into session state.
        st.session_state.profile = {
            "age": age,
            "gender": gender,
            "height_cm": height,
            "weight_kg": weight,
            "main_goal": main_goal,
            "sport": sport,
            "fitness_level": fitness_level,
            "training_days_per_week": training_days,
            "session_duration": session_duration,
            "injuries": injuries,
            "pain_rating": pain_rating,
        }
        # Move to the plan stage.
        st.session_state.stage = "plan"
        st.rerun()
