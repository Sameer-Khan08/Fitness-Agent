"""
settings.py
-----------
Loads environment variables from OS env, local .env file, or Streamlit secrets,
returning None safely if keys are missing.
"""

import os
from dotenv import load_dotenv

# Load all variables from the .env file into the environment if it exists.
try:
    load_dotenv(override=True)
except Exception:
    pass

def get_setting(key: str, default: str | None = None) -> str | None:
    """
    Safely retrieve a configuration value.
    First tries OS environment, then Streamlit secrets, falling back to default.
    """
    # 1. Check OS environment
    val = os.getenv(key)
    if val is not None and val.strip() != "":
        return val

    # 2. Check Streamlit secrets
    try:
        import streamlit as st
        # check if running under streamlit and has secrets
        if hasattr(st, "secrets") and key in st.secrets:
            val = st.secrets[key]
            if val is not None and str(val).strip() != "":
                return str(val)
    except Exception:
        pass

    return default

# --- Load settings ---
OPENAI_API_KEY = get_setting("OPENAI_API_KEY")
IMAGE_MODEL_API_KEY = get_setting("IMAGE_MODEL_API_KEY")
TOGETHER_API_KEY = get_setting("TOGETHER_API_KEY") or IMAGE_MODEL_API_KEY
SUPABASE_URL = get_setting("SUPABASE_URL")
SUPABASE_KEY = get_setting("SUPABASE_KEY")
APP_ENV = get_setting("APP_ENV", "development")

# Support both CONNECTION_STRING and DATABASE_URL for Postgres pool
DATABASE_URL = get_setting("CONNECTION_STRING") or get_setting("DATABASE_URL")
