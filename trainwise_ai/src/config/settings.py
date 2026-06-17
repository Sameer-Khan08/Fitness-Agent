"""
settings.py
-----------
Loads environment variables from the .env file and validates
that required keys are present before the app starts.
"""

import os
from dotenv import load_dotenv

# Load all variables from the .env file into the environment.
load_dotenv()

# --- Load environment variables ---

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
IMAGE_MODEL_API_KEY = os.getenv("IMAGE_MODEL_API_KEY")
TOGETHER_API_KEY = os.getenv("TOGETHER_API_KEY")
APP_ENV = os.getenv("APP_ENV", "development")  # Default to "development" if not set.

# --- Validate required keys ---

missing_keys = []

if not OPENAI_API_KEY:
    missing_keys.append("OPENAI_API_KEY")

# TOGETHER_API_KEY and IMAGE_MODEL_API_KEY are optional at startup —
# image generation will fail gracefully if not set.

if missing_keys:
    raise EnvironmentError(
        f"The following required environment variables are missing or empty: "
        f"{', '.join(missing_keys)}. "
        f"Please fill them in your .env file before running the app."
    )
