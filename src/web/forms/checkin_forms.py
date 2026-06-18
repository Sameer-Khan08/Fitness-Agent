"""
checkin_forms.py
----------------
Parsing logic for daily check-in form submissions.
"""


def parse_checkin_form(form) -> dict:
    """Parse daily check-in form data."""
    try:
        soreness = int(form.get("soreness", 0))
    except (TypeError, ValueError):
        soreness = 0
    try:
        stress = int(form.get("stress", 0))
    except (TypeError, ValueError):
        stress = 0
    try:
        pain_rating = int(form.get("pain_rating", 0))
    except (TypeError, ValueError):
        pain_rating = 0

    return {
        "sleep_quality": form.get("sleep_quality", "okay"),
        "energy_level": form.get("energy_level", "medium"),
        "soreness": max(0, min(10, soreness)),
        "stress": max(0, min(10, stress)),
        "pain_rating": max(0, min(10, pain_rating)),
        "pain_area": form.get("pain_area", "").strip(),
        "pain_trend": form.get("pain_trend", "same"),
        "trained_yesterday": form.get("trained_yesterday", "no"),
        "ready_to_train": form.get("ready_to_train", "yes"),
    }
