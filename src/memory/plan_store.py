"""
plan_store.py
-------------
Handles saving and retrieving generated training plans via Flask session.
"""

import datetime

from src.web.helpers import get_session_value, set_session_value


def save_plan_local(plan: dict) -> None:
    """Save a plan to Flask session."""
    saved = get_session_value("saved_plans", [])
    if not isinstance(saved, list):
        saved = []

    plan_with_meta = dict(plan)
    plan_with_meta["saved_at"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    saved.append(plan_with_meta)
    set_session_value("saved_plans", saved)


def get_saved_plans_local() -> list[dict]:
    """Retrieve all plans from Flask session."""
    saved = get_session_value("saved_plans", [])
    return saved if isinstance(saved, list) else []


def clear_saved_plans_local() -> None:
    """Clear all saved plans from Flask session."""
    set_session_value("saved_plans", [])
