"""
helpers.py
----------
General UI/layout helper integrations and fallback session setters/geters.
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
    session.modified = True


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
