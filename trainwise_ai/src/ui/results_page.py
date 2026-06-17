"""
results_page.py
---------------
Renders the results page with a rich display of the AI-generated
weekly workout plan, including exercise tables, on-demand demo images,
coaching notes, nutrition tips, and safety warnings.

Exercise images are generated via Together AI and cached in session state
so repeated clicks don't trigger a new API call.
"""

import streamlit as st

from src.exercises.image_prompts import generate_exercise_image
from src.ui.components import show_medical_disclaimer


def _get_image_cache() -> dict:
    """
    Return (and initialise if needed) the session-state image cache.
    Keys are exercise names, values are raw image bytes.
    """
    if "image_cache" not in st.session_state:
        st.session_state.image_cache = {}
    return st.session_state.image_cache


def _render_exercise_row(exercise: dict, session_idx: int, ex_idx: int) -> None:
    """
    Render a single exercise row: details on the left, demo button on the right.
    When the demo button is clicked, generate and display the image below.

    Args:
        exercise:    Exercise dict with name, sets, reps, rest, notes.
        session_idx: Index of the parent session (for unique widget keys).
        ex_idx:      Index of the exercise within its session.
    """
    name = exercise.get("name", "Exercise")
    sets = exercise.get("sets", "—")
    reps = exercise.get("reps", "—")
    rest = exercise.get("rest", "—")
    notes = exercise.get("notes", "")

    # Unique key for this exercise's demo button and image state.
    demo_key = f"demo_{session_idx}_{ex_idx}_{name.replace(' ', '_').lower()}"

    col_info, col_btn = st.columns([4, 1])

    with col_info:
        st.markdown(
            f"**{name}** &nbsp;·&nbsp; {sets} sets &nbsp;×&nbsp; {reps} reps "
            f"&nbsp;·&nbsp; Rest: {rest}"
        )
        if notes:
            st.caption(f"💡 {notes}")

    with col_btn:
        if st.button("📸 Demo", key=f"btn_{demo_key}", use_container_width=True):
            # Toggle the show-state for this exercise's image.
            toggle_key = f"show_{demo_key}"
            st.session_state[toggle_key] = not st.session_state.get(toggle_key, False)

    # Check if this exercise's image should be shown.
    show_key = f"show_{demo_key}"
    if st.session_state.get(show_key, False):
        image_cache = _get_image_cache()

        if name not in image_cache:
            # Generate and cache the image.
            with st.spinner(f"Generating demo for **{name}**..."):
                try:
                    image_bytes = generate_exercise_image(name)
                    image_cache[name] = image_bytes
                except EnvironmentError as e:
                    st.warning(f"⚙️ {e}")
                    st.session_state[show_key] = False
                except RuntimeError as e:
                    st.error(f"❌ Image generation failed: {e}")
                    st.session_state[show_key] = False

        if name in image_cache:
            st.image(
                image_cache[name],
                caption=f"{name} — Exercise demonstration",
                use_container_width=True,
            )


def _render_exercises(exercises: list[dict], session_idx: int) -> None:
    """
    Render all exercises for a session with details and demo image buttons.

    Args:
        exercises:   List of exercise dicts.
        session_idx: Index of the parent session for unique widget keys.
    """
    if not exercises:
        st.caption("No exercises listed for this session.")
        return

    # Table header
    st.markdown(
        "<div style='display:grid; grid-template-columns:4fr 1fr; "
        "font-weight:600; border-bottom:1px solid #444; padding-bottom:4px; "
        "margin-bottom:8px;'>"
        "<span>Exercise · Sets × Reps · Rest</span><span>Demo</span></div>",
        unsafe_allow_html=True,
    )

    for ex_idx, exercise in enumerate(exercises):
        _render_exercise_row(exercise, session_idx, ex_idx)
        if ex_idx < len(exercises) - 1:
            st.markdown("<hr style='margin:6px 0; opacity:0.15;'>", unsafe_allow_html=True)


def render_results_page() -> None:
    """
    Display the AI-generated workout plan with per-exercise image demo buttons.
    """
    st.title("🏋️ TrainWise AI")
    st.subheader("Your Personalised Plan")
    st.markdown("---")

    plan = st.session_state.get("results")

    # ── Fallback if no plan ──────────────────────────────────────────────────
    if not plan or not isinstance(plan, dict):
        st.warning("No plan found. Please generate a plan first.")
        if st.button("← Back to Plan Page"):
            st.session_state.stage = "plan"
            st.rerun()
        return

    # ── Red Flag Warnings (always first) ─────────────────────────────────────
    red_flags = plan.get("red_flag_warnings", [])
    if red_flags:
        st.error("🚨 **Important Safety Warnings**")
        for warning in red_flags:
            st.error(warning)
        st.markdown("---")

    # ── Plan Summary ─────────────────────────────────────────────────────────
    summary = plan.get("summary", "")
    if summary:
        st.markdown("### 📋 Plan Overview")
        st.info(summary)
        st.markdown("")

    # ── Weekly Schedule ──────────────────────────────────────────────────────
    weekly_schedule = plan.get("weekly_schedule", [])

    if weekly_schedule:
        st.markdown("### 📅 Weekly Schedule")
        st.caption(
            f"{len(weekly_schedule)} session(s) planned  ·  "
            "Click **📸 Demo** on any exercise to see a demonstration image"
        )
        st.markdown("")

        for i, session in enumerate(weekly_schedule):
            day = session.get("day", f"Day {i + 1}")
            session_type = session.get("session_type", "Training Session")
            duration = session.get("duration_minutes", "—")
            warm_up = session.get("warm_up", "")
            exercises = session.get("exercises", [])
            cool_down = session.get("cool_down", "")
            coaching_note = session.get("coaching_note", "")

            with st.expander(
                f"**{day}** — {session_type}  ·  ⏱ {duration} min",
                expanded=(i == 0),
            ):
                if warm_up:
                    st.markdown(f"**🔥 Warm-Up:** {warm_up}")
                    st.markdown("")

                st.markdown("**💪 Exercises**")
                _render_exercises(exercises, session_idx=i)

                if cool_down:
                    st.markdown("")
                    st.markdown(f"**🧊 Cool-Down:** {cool_down}")

                if coaching_note:
                    st.markdown("")
                    st.success(f"💬 **Coach's Note:** {coaching_note}")

        st.markdown("---")
    else:
        st.warning("No weekly schedule was returned by the AI.")

    # ── Injury Notes ─────────────────────────────────────────────────────────
    injury_notes = plan.get("injury_notes", "")
    if injury_notes:
        st.markdown("### 🩹 Injury Management Guidance")
        st.warning(injury_notes)
        st.markdown("")

    # ── Nutrition Tip ─────────────────────────────────────────────────────────
    nutrition_tip = plan.get("nutrition_tip", "")
    if nutrition_tip:
        st.markdown("### 🥗 Nutrition Tip")
        st.success(f"🥦 {nutrition_tip}")
        st.markdown("")

    # ── Recovery Advice ───────────────────────────────────────────────────────
    recovery_advice = plan.get("recovery_advice", "")
    if recovery_advice:
        st.markdown("### 😴 Recovery Advice")
        st.info(f"🔄 {recovery_advice}")
        st.markdown("")

    # ── Medical Disclaimer ────────────────────────────────────────────────────
    st.markdown("---")
    show_medical_disclaimer()
    st.warning(
        "🩺 **Medical Notice:** This app does not diagnose injuries. "
        "For serious or worsening symptoms, please consult a qualified doctor, "
        "physiotherapist, or healthcare professional before continuing any training."
    )

    # ── Navigation ────────────────────────────────────────────────────────────
    st.markdown("---")
    col1, col2 = st.columns(2)

    with col1:
        if st.button("🔄 Generate New Plan", use_container_width=True, type="primary"):
            st.session_state.stage = "plan"
            st.rerun()

    with col2:
        if st.button("← Start Over", use_container_width=True):
            st.session_state.stage = "onboarding"
            st.session_state.profile = None
            st.session_state.results = []
            st.session_state.image_cache = {}
            st.rerun()
