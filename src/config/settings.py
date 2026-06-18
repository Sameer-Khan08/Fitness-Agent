"""
settings.py
-----------
Global configuration loader and settings for TrainWise AI.
"""

import os
from dotenv import load_dotenv

# Environment Loading
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


# Flask Settings
APP_ENV = get_setting("APP_ENV", "development")
FLASK_SECRET_KEY = get_setting("FLASK_SECRET_KEY", "trainwise-dev-secret-change-in-production")

# App Mode & Feature Flags
DESIGN_MODE = get_setting("DESIGN_MODE", "false").lower() in ("true", "1", "yes")

default_coach_enabled = "false" if DESIGN_MODE else "true"
default_images_enabled = "false" if DESIGN_MODE else "true"

AI_COACH_ENABLED = get_setting("AI_COACH_ENABLED", default_coach_enabled).lower() in ("true", "1", "yes")
EXERCISE_IMAGES_ENABLED = get_setting("EXERCISE_IMAGES_ENABLED", default_images_enabled).lower() in ("true", "1", "yes")

# API Keys & Connections
TOGETHER_API_KEY = get_setting("TOGETHER_API_KEY")
IMAGE_MODEL_API_KEY = get_setting("IMAGE_MODEL_API_KEY")
SUPABASE_URL = get_setting("SUPABASE_URL")
SUPABASE_KEY = get_setting("SUPABASE_KEY")

# Database Settings
DATABASE_URL = get_setting("CONNECTION_STRING") or get_setting("DATABASE_URL")

# Clear Booleans for Availability
TEXT_AI_AVAILABLE = bool(TOGETHER_API_KEY)
IMAGE_AI_AVAILABLE = bool(TOGETHER_API_KEY or IMAGE_MODEL_API_KEY)
SUPABASE_AVAILABLE = bool(SUPABASE_URL and SUPABASE_KEY)

# Active Features
TEXT_AI_ENABLED = TEXT_AI_AVAILABLE and AI_COACH_ENABLED
IMAGE_AI_ENABLED = IMAGE_AI_AVAILABLE and EXERCISE_IMAGES_ENABLED

# Providers
AI_COACH_PROVIDER = "Together AI" if TEXT_AI_ENABLED else ("Design Mode" if DESIGN_MODE else "Offline")
IMAGE_PROVIDER = "Together AI" if IMAGE_AI_ENABLED else ("Design Mode" if DESIGN_MODE else "Offline")
