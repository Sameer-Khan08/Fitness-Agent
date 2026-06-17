"""
components.py
-------------
Shared UI helper components and styles used across the TrainWise AI application.
Provides custom CSS injection and reusable cards, badges, and templates.
"""

import streamlit as st
from src.exercises.image_prompts import generate_exercise_image


def inject_custom_css() -> None:
    """
    Inject premium dark athletic theme styling into the Streamlit app.
    """
    st.markdown(
        """
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700;800&display=swap');
            
            /* Enforce global font */
            html, body, [data-testid="stAppViewContainer"], .stWidget, .stMarkdown {
                font-family: 'Outfit', sans-serif !important;
            }
            
            /* Title & Header margins */
            h1, h2, h3, h4, h5, h6 {
                font-family: 'Outfit', sans-serif !important;
                font-weight: 700 !important;
                letter-spacing: -0.5px !important;
            }
            
            /* Premium Fitness Card styling */
            .fitness-card {
                background-color: #12161F;
                border: 1px solid rgba(255, 255, 255, 0.08);
                border-radius: 12px;
                padding: 22px;
                margin-bottom: 20px;
                box-shadow: 0 6px 16px rgba(0, 0, 0, 0.25);
            }
            
            /* Metrics Cards */
            .metric-card {
                background-color: #1E222B;
                border: 1px solid rgba(255, 255, 255, 0.06);
                border-radius: 10px;
                padding: 16px;
                text-align: center;
                margin-bottom: 12px;
                transition: transform 0.2s ease, border-color 0.2s ease;
            }
            .metric-card:hover {
                transform: translateY(-2px);
                border-color: rgba(0, 255, 135, 0.4);
            }
            
            /* Custom Badges */
            .status-badge {
                display: inline-block;
                padding: 6px 14px;
                border-radius: 30px;
                font-size: 13px;
                font-weight: 700;
                text-transform: uppercase;
                letter-spacing: 0.5px;
                margin: 4px 0;
            }
            .badge-ready {
                background-color: rgba(0, 255, 135, 0.12);
                color: #00FF87;
                border: 1px solid rgba(0, 255, 135, 0.3);
            }
            .badge-modify {
                background-color: rgba(255, 215, 0, 0.12);
                color: #FFD700;
                border: 1px solid rgba(255, 215, 0, 0.3);
            }
            .badge-stop {
                background-color: rgba(255, 75, 75, 0.12);
                color: #FF4B4B;
                border: 1px solid rgba(255, 75, 75, 0.3);
            }
            .badge-review {
                background-color: rgba(140, 150, 168, 0.12);
                color: #8C96A8;
                border: 1px solid rgba(140, 150, 168, 0.3);
            }
            
            /* Custom Warning / Info Cards */
            .warning-card {
                background-color: rgba(255, 75, 75, 0.07);
                border: 1px solid rgba(255, 75, 75, 0.2);
                border-radius: 8px;
                padding: 14px 18px;
                margin-bottom: 15px;
            }
            
            .info-card {
                background-color: rgba(96, 239, 255, 0.07);
                border: 1px solid rgba(96, 239, 255, 0.2);
                border-radius: 8px;
                padding: 14px 18px;
                margin-bottom: 15px;
            }
            
            /* Streamlit Form visual wrap */
            [data-testid="stForm"] {
                background-color: #12161F;
                border: 1px solid rgba(255, 255, 255, 0.08) !important;
                border-radius: 14px !important;
                padding: 30px !important;
                box-shadow: 0 8px 24px rgba(0, 0, 0, 0.3) !important;
            }
            
            /* Button overrides to look premium and action-oriented */
            div.stButton > button:first-child {
                background: linear-gradient(135deg, #1A1F2C 0%, #151924 100%) !important;
                color: #FFFFFF !important;
                border: 1px solid rgba(255, 255, 255, 0.12) !important;
                border-radius: 8px !important;
                font-weight: 600 !important;
                padding: 0.55rem 1.6rem !important;
                font-size: 14px !important;
                transition: all 0.25s ease !important;
                cursor: pointer;
            }
            
            div.stButton > button:first-child:hover {
                border-color: #00FF87 !important;
                box-shadow: 0px 4px 14px rgba(0, 255, 135, 0.18) !important;
                transform: translateY(-1px);
            }
            
            /* Primary action button accent overrides */
            div.stButton > button[kind="primary"] {
                background: linear-gradient(135deg, #00FF87 0%, #60EFFF 100%) !important;
                color: #0E1117 !important;
                font-weight: 700 !important;
                border: none !important;
                box-shadow: 0px 4px 12px rgba(0, 255, 135, 0.25) !important;
            }
            
            div.stButton > button[kind="primary"]:hover {
                transform: translateY(-2px);
                box-shadow: 0px 6px 20px rgba(0, 255, 135, 0.45) !important;
                color: #0E1117 !important;
            }
            
            /* Hide Streamlit default interface clutter */
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
        </style>
        """,
        unsafe_allow_html=True
    )


def hero_section(title: str, subtitle: str) -> None:
    """
    Renders a premium landing header block.
    """
    st.markdown(
        f"""
        <div style="text-align: center; padding: 25px 10px 35px 10px; margin-bottom: 20px;">
            <h1 style="font-size: 2.8rem; font-weight: 800; background: linear-gradient(135deg, #00FF87 0%, #60EFFF 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom: 12px; line-height: 1.2;">
                {title}
            </h1>
            <p style="font-size: 1.1rem; color: #8C96A8; max-width: 680px; margin: 0 auto; line-height: 1.5;">
                {subtitle}
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )


def section_header(title: str, subtitle: str | None = None) -> None:
    """
    Renders a clean, modern section header.
    """
    st.markdown(
        f"""
        <div style="margin-top: 30px; margin-bottom: 15px; border-bottom: 1px solid rgba(255, 255, 255, 0.08); padding-bottom: 8px;">
            <h3 style="margin: 0; color: #FFFFFF; font-size: 1.45rem;">{title}</h3>
            {f'<p style="margin: 4px 0 0 0; font-size: 0.9rem; color: #8C96A8;">{subtitle}</p>' if subtitle else ''}
        </div>
        """,
        unsafe_allow_html=True
    )


def metric_card(label: str, value: str, helper: str = "") -> None:
    """
    Renders a compact dashboard style metric.
    """
    st.markdown(
        f"""
        <div class="metric-card">
            <span style="color: #8C96A8; font-size: 11px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.8px;">{label}</span>
            <div style="color: #60EFFF; font-size: 20px; font-weight: 800; margin: 6px 0;">{value}</div>
            {f'<span style="color: #5C6470; font-size: 11px;">{helper}</span>' if helper else ''}
        </div>
        """,
        unsafe_allow_html=True
    )


def profile_card(profile: dict) -> None:
    """
    Renders an athlete profile summary card with all biological and training stats.
    """
    goal = profile.get("main_goal", "General Fitness")
    sport = profile.get("sport", "None") or "None"
    level = profile.get("fitness_level", "Beginner")
    days = profile.get("training_days_per_week", 3)
    pain = profile.get("pain_rating", 0)
    age = profile.get("age", "—")
    gender = profile.get("gender", "—")
    height = profile.get("height_cm", "—")
    weight = profile.get("weight_kg", "—")

    pain_color = "#00FF87" if pain == 0 else "#FFD700" if pain <= 4 else "#FF8C00" if pain <= 7 else "#FF4B4B"

    st.markdown(
        f"""
        <div class="fitness-card">
            <h4 style="margin-top: 0; color: #00FF87; border-bottom: 1px solid rgba(255,255,255,0.08); padding-bottom: 10px; font-size: 1.1rem; text-transform: uppercase; letter-spacing: 0.5px;">👤 Athlete Profile Summary</h4>
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(140px, 1fr)); gap: 18px; margin-top: 15px;">
                <div>
                    <span style="color: #8C96A8; font-size: 11px; font-weight: 600; text-transform: uppercase;">Goal</span><br/>
                    <strong style="font-size: 15px; color: white;">🎯 {goal}</strong>
                </div>
                <div>
                    <span style="color: #8C96A8; font-size: 11px; font-weight: 600; text-transform: uppercase;">Sport Focus</span><br/>
                    <strong style="font-size: 15px; color: white;">🏅 {sport}</strong>
                </div>
                <div>
                    <span style="color: #8C96A8; font-size: 11px; font-weight: 600; text-transform: uppercase;">Fitness Level</span><br/>
                    <strong style="font-size: 15px; color: white;">⚡ {level}</strong>
                </div>
                <div>
                    <span style="color: #8C96A8; font-size: 11px; font-weight: 600; text-transform: uppercase;">Weekly Frequency</span><br/>
                    <strong style="font-size: 15px; color: white;">📅 {days} Days</strong>
                </div>
                <div>
                    <span style="color: #8C96A8; font-size: 11px; font-weight: 600; text-transform: uppercase;">Pain Rating</span><br/>
                    <strong style="font-size: 15px; color: {pain_color};">🛡️ {pain}/10</strong>
                </div>
                <div>
                    <span style="color: #8C96A8; font-size: 11px; font-weight: 600; text-transform: uppercase;">Biometrics</span><br/>
                    <strong style="font-size: 14px; color: white;">🎂 {age}y | 📏 {height}cm | ⚖️ {weight}kg</strong>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


def safety_card(safety: dict, medical: dict) -> None:
    """
    Renders readiness status and warning info.
    """
    status = safety.get("status", "Green")
    summary = safety.get("summary", "")
    warnings = medical.get("warnings", [])
    message = medical.get("message", "")

    if status.lower() in ["green", "ready"]:
        color = "#00FF87"
        bg = "rgba(0, 255, 135, 0.08)"
        label = "Ready to Train"
    elif status.lower() in ["yellow", "modify"]:
        color = "#FFD700"
        bg = "rgba(255, 215, 0, 0.08)"
        label = "Modify Training"
    else:
        color = "#FF4B4B"
        bg = "rgba(255, 75, 75, 0.08)"
        label = "Do Not Push Intensity"

    st.markdown(
        f"""
        <div style="border-left: 5px solid {color}; background-color: {bg}; padding: 18px; border-radius: 8px; margin-bottom: 22px; box-shadow: 0 4px 12px rgba(0,0,0,0.15);">
            <h4 style="color: {color}; margin-top: 0; margin-bottom: 8px; display: flex; align-items: center; gap: 8px; font-size: 1.15rem;">
                <span>📊</span> Safety Status: {label}
            </h4>
            <p style="margin: 0; font-size: 14px; line-height: 1.6; color: #E0E0E0;">{summary}</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    if warnings:
        for w in warnings:
            st.error(w)
    elif message:
        st.warning(message)


def workout_day_card(day_plan: dict, day_idx: int = 0) -> None:
    """
    Renders a premium visual card showing a full day's training program,
    incorporating session type, warm-up, exercises with dropdown expanders, and recovery.
    """
    day = day_plan.get("day", f"Day {day_idx + 1}")
    session_type = day_plan.get("session_type", "Training Session")
    session_goal = day_plan.get("session_goal", "")
    duration = day_plan.get("duration_minutes", "—")
    warm_up = day_plan.get("warm_up", "")
    exercises = day_plan.get("exercises", [])
    cool_down = day_plan.get("cool_down", "")
    coaching = day_plan.get("coaching_note", "")
    
    # Check if intensity is specified in the schedule, else default
    intensity = day_plan.get("intensity", "Moderate")

    # Header Card Segment
    st.markdown(
        f"""
        <div style="background: linear-gradient(135deg, #181B22 0%, #12161F 100%); border: 1px solid rgba(255, 255, 255, 0.07); border-radius: 12px 12px 0 0; padding: 18px 22px; border-bottom: 2px solid #00FF87;">
            <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 10px;">
                <h4 style="margin: 0; color: #00FF87; font-size: 1.25rem;">📅 {day}</h4>
                <span style="background-color: rgba(96, 239, 255, 0.12); color: #60EFFF; font-size: 11px; font-weight: 700; padding: 4px 10px; border-radius: 12px; text-transform: uppercase; letter-spacing: 0.5px;">⏱ {duration} MIN</span>
            </div>
            <h5 style="margin: 10px 0 6px 0; color: white; font-size: 1.05rem;">🎯 {session_type}</h5>
            {f'<p style="margin: 0 0 8px 0; font-size: 13px; color: #8C96A8; font-style: italic; line-height: 1.4;">{session_goal}</p>' if session_goal else ''}
            <div style="margin-top: 8px; font-size: 11px; letter-spacing: 0.5px;">
                <span style="color: #8C96A8; font-weight: 700; text-transform: uppercase;">Intensity:</span> 
                <span style="color: #FFD700; font-weight: bold; text-transform: uppercase;">{intensity}</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Content Container wrapper
    st.markdown(
        """
        <div style="background-color: #0E1117; border: 1px solid rgba(255, 255, 255, 0.07); border-top: none; border-radius: 0 0 12px 12px; padding: 20px 22px; margin-bottom: 25px; box-shadow: 0 4px 12px rgba(0,0,0,0.18);">
        """,
        unsafe_allow_html=True
    )

    # Session Elements
    if warm_up:
        st.markdown(f"**🔥 Warm-Up:** {warm_up}")
        st.markdown("<hr style='margin:12px 0; opacity:0.08;'>", unsafe_allow_html=True)

    if exercises:
        st.markdown("**💪 Exercises**")
        for ex_idx, exercise in enumerate(exercises):
            name = exercise.get("name", "Exercise")
            sets = exercise.get("sets", "—")
            reps = exercise.get("reps", "—")
            rest = exercise.get("rest", "—")
            notes = exercise.get("notes", "")
            why_you = exercise.get("why_you", "")
            
            # Label
            st.markdown(
                f"<div style='margin-top: 8px;'>🏋️ <strong>{name}</strong> · "
                f"<span style='color: #60EFFF;'>{sets} Sets × {reps} Reps</span> (Rest: {rest})</div>",
                unsafe_allow_html=True
            )
            
            # View Instructions
            with st.expander("📝 View Instructions & Demo", expanded=False):
                if notes:
                    st.markdown(f"**Technique Cue:** *{notes}*")
                if why_you:
                    st.markdown(
                        f"<div class='info-card' style='margin: 8px 0;'>"
                        f"<strong>Why this for you:</strong> {why_you}"
                        f"</div>",
                        unsafe_allow_html=True
                    )
                
                # Image Demo
                demo_key = f"demo_{day_idx}_{ex_idx}_{name.replace(' ', '_').lower()}"
                show_key = f"show_{demo_key}"
                
                col_btn, _ = st.columns([1, 2])
                with col_btn:
                    if st.button("📸 Demo Image", key=f"btn_{demo_key}", width="stretch"):
                        st.session_state[show_key] = not st.session_state.get(show_key, False)
                        
                if st.session_state.get(show_key, False):
                    image_cache = st.session_state.setdefault("image_cache", {})
                    if name not in image_cache:
                        with st.spinner("Generating demo image..."):
                            try:
                                image_bytes = generate_exercise_image(name)
                                image_cache[name] = image_bytes
                            except Exception as e:
                                st.error(f"Image generation failed: {e}")
                                
                    if name in image_cache:
                        st.image(image_cache[name], caption=f"{name} demo", width="stretch")
            
            if ex_idx < len(exercises) - 1:
                st.markdown("<hr style='margin:10px 0; opacity:0.04;'>", unsafe_allow_html=True)
    else:
        st.caption("No exercises programmed.")

    if cool_down:
        st.markdown("<hr style='margin:12px 0; opacity:0.08;'>", unsafe_allow_html=True)
        st.markdown(f"**🧊 Cool-Down:** {cool_down}")

    if coaching:
        st.markdown("<hr style='margin:12px 0; opacity:0.08;'>", unsafe_allow_html=True)
        st.markdown(
            f"<div class='info-card' style='margin-bottom: 0;'>"
            f"<strong>💬 Coach's Advice:</strong> {coaching}"
            f"</div>",
            unsafe_allow_html=True
        )

    st.markdown("</div>", unsafe_allow_html=True)


def show_medical_disclaimer() -> None:
    """
    Standard warning disclaimer for health / exercise liability.
    """
    st.markdown(
        """
        <div class="warning-card" style="border-left: 5px solid #FF4B4B; margin-bottom: 20px;">
            <strong style="color: #FF4B4B; font-size: 14px;">🛡️ Safety & Medical Disclaimer</strong>
            <p style="margin: 6px 0 0 0; font-size: 13px; line-height: 1.5; color: #E0E0E0;">
                This tool provides general fitness guidance only. It is not a medical diagnosis or treatment plan. 
                For severe, worsening, sharp, or unusual symptoms, consult a qualified doctor or physiotherapist.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )


def render_status_badge(status: str) -> None:
    """
    Renders status badge using Streamlit feedback blocks.
    """
    status_lower = status.lower()
    if "green" in status_lower or "ready" in status_lower:
        st.success("🟢 Ready to Train")
    elif "yellow" in status_lower or "modify" in status_lower:
        st.warning("🟡 Modify Training")
    elif "red" in status_lower or "stop" in status_lower or "seek" in status_lower:
        st.error("🔴 Stop / Seek Help")
    else:
        st.info("⚪ Review Required")
