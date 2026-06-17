"""
image_prompts.py
----------------
Handles exercise demonstration image generation using the
Together AI client with the openai/gpt-image-1 model.

Images are returned as raw bytes (decoded from base64) so they
can be displayed directly in Streamlit via st.image().
"""

import base64
from together import Together

from src.config.settings import TOGETHER_API_KEY

# Together AI image model to use.
IMAGE_MODEL = "black-forest-labs/FLUX.1-schnell-Free"


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


def generate_exercise_image(exercise_name: str) -> bytes:
    """
    Generate a demonstration image for the given exercise using Together AI.

    Args:
        exercise_name: The name of the exercise to illustrate.

    Returns:
        Raw image bytes (PNG) decoded from the base64 API response.

    Raises:
        EnvironmentError: If TOGETHER_API_KEY is not set.
        RuntimeError:     If the API call fails or returns no image data.
    """
    if not TOGETHER_API_KEY:
        raise EnvironmentError(
            "TOGETHER_API_KEY is not set in your .env file. "
            "Please add your Together AI API key to enable exercise images."
        )

    prompt = build_exercise_image_prompt(exercise_name)

    try:
        client = Together(api_key=TOGETHER_API_KEY)
        response = client.images.generate(
            prompt=prompt,
            model=IMAGE_MODEL,
            width=768,
            height=512,
            steps=4,
            n=1,
        )
    except Exception as e:
        raise RuntimeError(
            f"Together AI image generation failed for '{exercise_name}': {e}"
        ) from e

    # Extract base64 image data from the response.
    if not response.data or not response.data[0].b64_json:
        raise RuntimeError(
            f"Together AI returned an empty response for '{exercise_name}'. "
            "No image data was included."
        )

    raw_b64 = response.data[0].b64_json
    image_bytes = base64.b64decode(raw_b64)
    return image_bytes
