"""
image_prompts.py
----------------
Handles exercise demonstration image generation using the
Together AI client.

Primary model  : openai/gpt-image-1.5  (high quality)
Fallback model : black-forest-labs/FLUX.1-schnell (fast, serverless)

The API may return images as either base64 JSON or a hosted URL.
Both cases are handled automatically.

Images are returned as raw bytes so they can be displayed directly
in Streamlit via st.image().
"""

import base64
import requests as _requests
from together import Together

from src.config.settings import TOGETHER_API_KEY

# Primary model — as specified in project requirements.
IMAGE_MODEL_PRIMARY = "openai/gpt-image-1.5"

# Fallback model — fast, serverless, always available.
IMAGE_MODEL_FALLBACK = "black-forest-labs/FLUX.1-schnell"

# Request timeout for fetching hosted image URLs (seconds).
_URL_FETCH_TIMEOUT = 30


def build_exercise_image_prompt(exercise_name: str) -> str:
    """
    Build a descriptive prompt for generating a realistic exercise
    demonstration image.

    Args:
        exercise_name: The name of the exercise to demonstrate.

    Returns:
        A prompt string for the image generation model.
    """
    prompt = (
        f"A realistic photograph of a fit athlete performing the {exercise_name} exercise "
        f"with perfect form. "
        "Clean modern gym setting with neutral background and soft professional lighting. "
        "Full body visible, clear movement demonstration showing correct posture and alignment. "
        "High quality, photorealistic, fitness magazine style. "
        "No text, no labels, no watermarks, no overlays in the image."
    )
    return prompt


def _extract_image_bytes(response) -> bytes:
    """
    Extract raw image bytes from a Together AI image response.

    Handles both base64 (b64_json) and hosted URL (url) response formats.

    Args:
        response: The Together AI images.generate() response object.

    Returns:
        Raw image bytes.

    Raises:
        RuntimeError: If neither b64_json nor url is present in the response.
    """
    item = response.data[0]

    # Case 1: base64-encoded image returned directly.
    if item.b64_json:
        return base64.b64decode(item.b64_json)

    # Case 2: hosted URL returned — download the image.
    if item.url:
        resp = _requests.get(item.url, timeout=_URL_FETCH_TIMEOUT)
        resp.raise_for_status()
        return resp.content

    raise RuntimeError(
        "Together AI response contained neither b64_json nor url. "
        "Cannot extract image data."
    )


def generate_exercise_image(exercise_name: str) -> bytes:
    """
    Generate a demonstration image for the given exercise using Together AI.

    Tries the primary model (openai/gpt-image-1.5) first, then falls back
    to FLUX.1-schnell if the primary is unavailable.

    Args:
        exercise_name: The name of the exercise to illustrate.

    Returns:
        Raw image bytes (PNG/JPEG) ready for display with st.image().

    Raises:
        EnvironmentError: If TOGETHER_API_KEY is not set.
        RuntimeError:     If both models fail to generate an image.
    """
    if not TOGETHER_API_KEY:
        raise EnvironmentError(
            "TOGETHER_API_KEY is not set in your .env file. "
            "Please add your Together AI API key to enable exercise demo images."
        )

    prompt = build_exercise_image_prompt(exercise_name)
    client = Together(api_key=TOGETHER_API_KEY)

    # ── Try primary model ────────────────────────────────────────────────────
    try:
        response = client.images.generate(
            prompt=prompt,
            model=IMAGE_MODEL_PRIMARY,
            n=1,
        )
        return _extract_image_bytes(response)

    except Exception as primary_error:
        # Primary model failed — try the fallback.
        pass

    # ── Try fallback model ───────────────────────────────────────────────────
    try:
        response = client.images.generate(
            prompt=prompt,
            model=IMAGE_MODEL_FALLBACK,
            width=768,
            height=512,
            steps=4,
            n=1,
        )
        return _extract_image_bytes(response)

    except Exception as fallback_error:
        raise RuntimeError(
            f"Image generation failed for '{exercise_name}'. "
            f"Primary model error: {primary_error}. "
            f"Fallback model error: {fallback_error}."
        ) from fallback_error
