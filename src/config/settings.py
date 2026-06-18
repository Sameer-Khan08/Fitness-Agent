"""
settings.py
-----------
Loads environment variables from OS env and local .env file,
returning None safely if keys are missing.
"""

import os
from dotenv import load_dotenv

try:
    load_dotenv(override=True)
except Exception:
    pass


def get_setting(key: str, default: str | None = None) -> str | None:
    """Safely retrieve a configuration value from the environment."""
    val = os.getenv(key)
    if val is not None and val.strip() != "":
        return val
    return default


IMAGE_MODEL_API_KEY = get_setting("IMAGE_MODEL_API_KEY")
TOGETHER_API_KEY = get_setting("TOGETHER_API_KEY")
SUPABASE_URL = get_setting("SUPABASE_URL")
SUPABASE_KEY = get_setting("SUPABASE_KEY")
APP_ENV = get_setting("APP_ENV", "development")
FLASK_SECRET_KEY = get_setting("FLASK_SECRET_KEY", "trainwise-dev-secret-change-in-production")

DATABASE_URL = get_setting("CONNECTION_STRING") or get_setting("DATABASE_URL")

TEXT_AI_ENABLED = bool(TOGETHER_API_KEY)
IMAGE_AI_ENABLED = bool(TOGETHER_API_KEY or IMAGE_MODEL_API_KEY)

AI_COACH_PROVIDER = "Together AI" if TOGETHER_API_KEY else "Offline"
IMAGE_PROVIDER = "Together AI" if TOGETHER_API_KEY or IMAGE_MODEL_API_KEY else "Offline"
