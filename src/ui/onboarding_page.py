"""
onboarding_page.py
------------------
Renders the redesign-based onboarding form where users enter their athlete profile.
Uses columns, clean sections, custom CSS styling, and dashboard cards.
"""

import streamlit as st
from src.ui.components import inject_custom_css, hero_section


def render_onboarding_page() -> None:
    """
    Display the redesigned onboarding page with a fitness/athletic profile form.
    On submission, saves the profile to session state and routes the user to the plan stage.
    """
    # 1. Custom CSS
    inject_custom_css()

    # 2. Hero Section
    hero_section(
        title="TrainWise AI",
        subtitle="AI-powered fitness and athletic performance planning with injury-aware reality checks."
    )
    st.subheader("Athlete Onboarding")

    # 3. How it Works cards
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(
            """
            <div class="metric-card" style="height: 130px;">
                <span style="font-size: 1.6rem;">🎯</span>
                <h5 style="margin: 6px 0 4px 0; color: white;">1. Tell us your goal</h5>
                <p style="font-size: 12px; color: #8C96A8; margin: 0;">Specify what you want to achieve or improve.</p>
            </div>
            """,
            unsafe_allow_html=True
        )
    with col2:
        st.markdown(
            """
            <div class="metric-card" style="height: 130px;">
                <span style="font-size: 1.6rem;">🩹</span>
                <h5 style="margin: 6px 0 4px 0; color: white;">2. Add Sport & Pain</h5>
                <p style="font-size: 12px; color: #8C96A8; margin: 0;">Add athletic and pain context for screen check.</p>
            </div>
            """,
            unsafe_allow_html=True
        )
    with col3:
        st.markdown(
            """
            <div class="metric-card" style="height: 130px;">
                <span style="font-size: 1.6rem;">⚡</span>
                <h5 style="margin: 6px 0 4px 0; color: white;">3. Get your plan</h5>
                <p style="font-size: 12px; color: #8C96A8; margin: 0;">Generate a custom, injury-aware coach routine.</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown("<br>", unsafe_allow_html=True)

    # 4. Form
    with st.form(key="onboarding_form"):
        
        # --- Section 1: Body Profile ---
        st.markdown("### 👤 Body Profile")
        col_age, col_gen = st.columns(2)
        with col_age:
            age = st.number_input(
                "Age (years)",
                min_value=12,
                max_value=100,
                value=25,
                step=1,
            )
        with col_gen:
            gender = st.selectbox(
                "Gender",
                options=["Male", "Female", "Other", "Prefer not to say"],
            )

        col_h, col_w = st.columns(2)
        with col_h:
            height = st.text_input("Height", value="170", placeholder="e.g. 170 or 5'9\"")
        with col_w:
            weight = st.text_input("Weight", value="70", placeholder="e.g. 70 or 154 lbs")

        st.markdown("<hr style='margin:20px 0; opacity:0.1;'>", unsafe_allow_html=True)

        # --- Section 2: Training Goal ---
        st.markdown("### 🎯 Training Goal")
        main_goal = st.selectbox(
            "Main Goal",
            options=[
                "Weight Loss",
                "Muscle Gain",
                "General Fitness",
                "Athletic Performance",
                "Sport-Specific Performance",
                "Strength",
                "Endurance",
                "Mobility",
            ],
        )

        fitness_level = st.selectbox(
            "Fitness Level",
            options=["Beginner", "Intermediate", "Advanced"],
        )

        # Retain the primary problem field from specificity overhaul as it drives AI diagnosis logic
        st.markdown("##### 🔍 Describe your exact situation (Primary Problem)")
        st.caption("Tell us exactly what you want to solve. Be as specific as possible.")
        primary_problem = st.text_area(
            "Primary problem or goal description",
            placeholder=(
                "Examples:\n"
                "• I've had left knee pain for 6 months. I can't squat without pain and I play football on weekends.\n"
                "• I've been training for 2 years but my bench press is stuck at 80kg and I can't seem to break through.\n"
                "• I run 3x a week but my calves cramp badly after 15 mins. I want to run a 5k in under 25 minutes."
            ),
            height=100,
            label_visibility="collapsed"
        )

        st.markdown("<hr style='margin:20px 0; opacity:0.1;'>", unsafe_allow_html=True)

        # --- Section 3: Sport & Schedule ---
        st.markdown("### 🏃 Sport & Schedule")
        sport = st.selectbox(
            "Sport Focus",
            options=[
                "None",
                "Gym Only",
                "Football",
                "Soccer",
                "Basketball",
                "Cricket",
                "Tennis",
                "Badminton",
                "Running",
                "Other",
            ],
        )

        training_days = st.slider(
            "Training days per week",
            min_value=2,
            max_value=7,
            value=3,
        )

        session_duration = st.selectbox(
            "Preferred session duration",
            options=["30 minutes", "45 minutes", "60 minutes", "75 minutes", "90 minutes"],
            index=2
        )

        st.markdown("<hr style='margin:20px 0; opacity:0.1;'>", unsafe_allow_html=True)

        # --- Section 4: Injury Reality Check ---
        st.markdown("### 🛡️ Injury Reality Check")
        injuries = st.text_area(
            "Describe any injuries or pain areas",
            placeholder="Example: groin pain during sprinting, knee pain when jumping, lower back pain during deadlifts",
            height=80,
        )

        pain_rating = st.slider(
            "Current pain rating",
            min_value=0,
            max_value=10,
            value=0,
            help="0 = no pain, 10 = worst pain imaginable"
        )
        st.caption("ℹ️ 0 = no pain, 10 = worst pain imaginable")

        st.markdown("<br>", unsafe_allow_html=True)
        submitted = st.form_submit_button("Build My Plan", width="stretch", type="primary")

    if submitted:
        # Fallback to general description if primary problem is empty
        prob_text = primary_problem.strip()
        if not prob_text:
            prob_text = f"Goal: {main_goal}. Sport: {sport}. Fitness level: {fitness_level}."

        profile_data = {
            "primary_problem": prob_text,
            "age": age,
            "gender": gender,
            "height_cm": height,
            "weight_kg": weight,
            "main_goal": main_goal,
            "goal": main_goal,  # alias for DB
            "sport": sport,
            "main_sport": sport,  # alias for DB
            "fitness_level": fitness_level,
            "training_days_per_week": training_days,
            "session_duration": session_duration,
            "injuries": injuries,
            "pain_rating": pain_rating,
        }
        st.session_state.profile = profile_data
        
        # Save to DB if logged in
        if st.session_state.get('user_id'):
            from database.save_new_user import save_user_profile_data
            save_user_profile_data(st.session_state.user_id, profile_data)
            
        st.session_state.stage = "plan"
        st.rerun()
