"""
helpers.py
----------
Helper functions for managing Flask session state and checking configuration statuses.
"""

import os
from flask import session
from src.config.settings import TEXT_AI_ENABLED, IMAGE_AI_ENABLED, SUPABASE_URL, SUPABASE_KEY


def get_session_value(key, default=None):
    """Retrieve a value from the Flask session."""
    return session.get(key, default)


def set_session_value(key, value):
    """Set a value in the Flask session."""
    session[key] = value


def init_session_defaults():
    """Initialize default session structure if not present."""
    if "profile" not in session:
        session["profile"] = None
    if "results" not in session:
        session["results"] = None
    if "saved_plans" not in session:
        session["saved_plans"] = []
    if "checkins" not in session:
        session["checkins"] = []
    if "image_cache" not in session:
        session["image_cache"] = {}
    if "generated_image_count" not in session:
        session["generated_image_count"] = 0


def clear_current_workflow():
    """Reset current workflow values, retaining saved plans and image cache."""
    session["profile"] = None
    session["results"] = None
    session["ai_explanation"] = None
    session["current_readiness"] = None
    session["adjusted_today_workout"] = None
    session["nutrition_result"] = None
    session["nutrition_ai_explanation"] = None


def get_current_profile():
    """Get the current profile from session."""
    return session.get("profile")


def get_current_results():
    """Get the current results/plan from session."""
    return session.get("results")


def has_profile():
    """Check if profile is present in session."""
    return bool(session.get("profile"))


def has_plan():
    """Check if plan/results are present in session."""
    return bool(session.get("results"))


def get_api_status():
    """Return configured API statuses for the sidebar."""
    return {
        "text_ai": bool(TEXT_AI_ENABLED),
        "images": bool(IMAGE_AI_ENABLED),
        "supabase": bool(SUPABASE_URL and SUPABASE_KEY),
    }


def get_deployment_checklist():
    """Check existence of essential files and configurations."""
    root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    return {
        "requirements_txt": os.path.exists(os.path.join(root_dir, "requirements.txt")),
        "env_example": os.path.exists(os.path.join(root_dir, ".env.example")),
        "readme": os.path.exists(os.path.join(root_dir, "README.md")),
        "text_ai": bool(TEXT_AI_ENABLED),
        "images": bool(IMAGE_AI_ENABLED),
        "supabase": bool(SUPABASE_URL and SUPABASE_KEY),
    }
