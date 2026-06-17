import streamlit as st
from src.ui.components import inject_custom_css, show_medical_disclaimer, section_header
from src.nutrition.nutrition_engine import estimate_nutrition_targets

def render_nutrition_page() -> None:
    inject_custom_css()
    st.title("TrainWise AI")
    st.subheader("Nutrition Guidance")
    st.markdown("---")

    profile = st.session_state.get("profile")
    if not profile:
        st.warning("Please complete the onboarding form to generate personalized nutrition estimates.")
        if st.button("Go to Onboarding"):
            st.session_state.stage = "onboarding"
            st.rerun()
        return

    # Calculate targets
    targets = estimate_nutrition_targets(profile)
    
    # Calorie display
    m_cals = targets.get("maintenance_calories")
    t_cals = targets.get("target_calories")
    prot = targets.get("protein_range_g", "—")
    hyd = targets.get("hydration", "—")

    st.markdown("### Caloric Baseline & Targets")
    col1, col2 = st.columns(2)
    with col1:
        if m_cals:
            st.metric("Estimated Maintenance", f"{m_cals} kcal/day")
        else:
            st.metric("Estimated Maintenance", "Unavailable")
    with col2:
        if t_cals:
            st.metric("Estimated Daily Target", f"{t_cals} kcal/day")
        else:
            st.metric("Estimated Daily Target", "Unavailable")

    # Protein & Hydration
    st.markdown("### Macronutrients & Hydration")
    st.markdown(f"🍗 **Protein Target**: {prot}")
    st.markdown(f"💧 **Hydration**: {hyd}")

    # Notes and Meal Structure
    st.markdown("### Meal Structure Guidelines")
    for item in targets.get("meal_structure", []):
        st.markdown(f"- {item}")

    if targets.get("notes"):
        st.markdown("### Coach Notes")
        for note in targets.get("notes", []):
            st.info(f"👉 {note}")

    # Disclaimer
    st.markdown("<br>", unsafe_allow_html=True)
    show_medical_disclaimer()

    # Navigation buttons
    st.markdown("<hr style='margin:20px 0; opacity:0.1;'>", unsafe_allow_html=True)
    b1, b2, b3 = st.columns(3)
    with b1:
        if st.button("← Fitness Plan", use_container_width=True):
            st.session_state.stage = "results" if st.session_state.get("results") else "plan"
            st.rerun()
    with b2:
        if st.button("⏱ Daily Check-in", use_container_width=True):
            st.session_state.stage = "checkin"
            st.rerun()
    with b3:
        if st.button("📊 Saved Plans", use_container_width=True):
            st.session_state.stage = "dashboard"
            st.rerun()
