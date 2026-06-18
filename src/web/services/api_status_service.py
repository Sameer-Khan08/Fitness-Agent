"""
api_status_service.py
---------------------
Determines connection state strings for system components like AI Coach, Exercise Visuals, and Cloud Storage.
"""

from src.config.settings import (
    DESIGN_MODE,
    TEXT_AI_ENABLED,
    IMAGE_AI_ENABLED,
    SUPABASE_AVAILABLE,
)


def get_api_status() -> dict:
    """Return dictionary with connection status strings for all system features."""
    if TEXT_AI_ENABLED:
        ai_coach = "Connected"
    elif DESIGN_MODE:
        ai_coach = "Design Mode"
    else:
        ai_coach = "Disabled"

    if IMAGE_AI_ENABLED:
        exercise_images = "Connected"
    elif DESIGN_MODE:
        exercise_images = "Design Mode"
    else:
        exercise_images = "Disabled"

    if SUPABASE_AVAILABLE:
        cloud_db = "Connected"
    elif DESIGN_MODE:
        cloud_db = "Design Mode"
    else:
        cloud_db = "Disabled"

    return {
        "ai_coach": ai_coach,
        "exercise_images": exercise_images,
        "cloud_db": cloud_db,
    }
