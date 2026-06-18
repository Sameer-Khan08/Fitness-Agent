"""
session_service.py
------------------
Clean, typed state management wrappers around Flask's session object.
"""

from flask import session


def init_session_defaults() -> None:
    """Initialize defaults in the Flask session dictionary if not already set."""
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


def get_profile() -> dict | None:
    """Retrieve the current user profile from session."""
    return session.get("profile")


def set_profile(profile: dict) -> None:
    """Save the current user profile to session."""
    session["profile"] = profile
    session.modified = True


def clear_profile() -> None:
    """Remove user profile from session."""
    session["profile"] = None
    session.modified = True


def get_results() -> dict | None:
    """Retrieve the generated plan results from session."""
    return session.get("results")


def set_results(results: dict) -> None:
    """Save the generated plan results to session."""
    session["results"] = results
    session.modified = True


def clear_results() -> None:
    """Remove generated plan results from session."""
    session["results"] = None
    session.modified = True


def get_saved_plans() -> list:
    """Retrieve the archived plans list from session."""
    return session.get("saved_plans", [])


def set_saved_plans(plans: list) -> None:
    """Update the archived plans list in session."""
    session["saved_plans"] = plans
    session.modified = True


def get_image_cache() -> dict:
    """Retrieve in-session image visual cache mapping."""
    return session.get("image_cache", {})


def set_image_cache(cache: dict) -> None:
    """Update in-session image visual cache mapping."""
    session["image_cache"] = cache
    session.modified = True


def get_generated_image_count() -> int:
    """Get count of images generated during this session."""
    return session.get("generated_image_count", 0)


def increment_generated_image_count() -> None:
    """Increment session counter for generated images."""
    session["generated_image_count"] = session.get("generated_image_count", 0) + 1
    session.modified = True


def clear_current_workflow() -> None:
    """Reset current user plan workflow data, keeping saved plans and caches."""
    session["profile"] = None
    session["results"] = None
    session["ai_explanation"] = None
    session["current_readiness"] = None
    session["adjusted_today_workout"] = None
    session["nutrition_result"] = None
    session["nutrition_ai_explanation"] = None
    session.modified = True
