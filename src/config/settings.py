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

# Note: For this MVP rule-based step, no API keys are strictly required at startup.
# We do not raise EnvironmentError if keys are missing.
