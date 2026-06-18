"""
checkin_store.py
----------------
Handles saving and retrieving daily check-ins in Flask session.
"""

import datetime

from src.web.helpers import get_session_value, set_session_value


def save_checkin_local(checkin: dict) -> None:
    """Save a check-in to Flask session."""
    checkins = get_session_value("checkins", [])
    if not isinstance(checkins, list):
        checkins = []

    checkin_with_meta = dict(checkin)
    checkin_with_meta["timestamp"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    checkins.append(checkin_with_meta)
    set_session_value("checkins", checkins)


def get_checkins_local() -> list[dict]:
    """Retrieve all check-ins from Flask session."""
    checkins = get_session_value("checkins", [])
    return checkins if isinstance(checkins, list) else []


def clear_checkins_local() -> None:
    """Clear all check-ins from Flask session."""
    set_session_value("checkins", [])
