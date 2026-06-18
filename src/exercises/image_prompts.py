"""
image_prompts.py
----------------
Handles exercise demonstration image generation using the
Together AI client.

Primary model  : black-forest-labs/FLUX.1.1-pro (high quality)
Fallback model : black-forest-labs/FLUX.1-schnell (fast, serverless)

The API may return images as either base64 JSON or a hosted URL.
Both cases are handled automatically.

Images are returned as raw bytes or base64 data URIs for display.
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
_URL_FETCH_TIMEOUT = 15


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
        # f"A realistic photograph of a fit athlete performing the {exercise_name} exercise "
        # f"with perfect form. "
        # "Clean modern gym setting with neutral background and soft professional lighting. "
        # "Full body visible, clear movement demonstration showing correct posture and alignment. "
        # "High quality, photorealistic, fitness magazine style. "
        # "Atleast one cycle of the movement should be visible. It should be a step-by-step infographic showing the steps of the exercise."
        # "No text, no watermarks, no overlays in the image."
        f"""
Create one photorealistic fitness exercise instruction image for **{exercise_name}**.

The output must be **one single image** divided into **4 clearly separated blocks/panels** in a clean **2x2 grid layout**.

### Layout requirements

* Panel 1 = **Step 1**
* Panel 2 = **Step 2**
* Panel 3 = **Step 3**
* Panel 4 = **Step 4**

Each panel must:

* show the **same real human athlete**
* show **only one body position**
* have **clear visual separation** from the other panels
* include a **small clean title label** at the top such as:

  * **Step 1: Start**
  * **Step 2: Lower**
  * **Step 3: Bottom Position**
  * **Step 4: Return**
* include **1–2 short form labels/cues** in each panel

### Form label requirements

Add short, clean instructional cues near the athlete, such as:

* **Chest up**
* **Neutral spine**
* **Knees track over toes**
* **Heels flat**
* **Core engaged**
* **Controlled descent**
* **Drive through heels**
* **Return to start**

Do not add long paragraphs.
Keep form labels very short, clean, and easy to read.
The labels should feel like a professional exercise instruction card.

### Visual style

* photorealistic
* realistic human anatomy
* clean modern gym background
* same camera angle in all 4 panels
* full body visible in every panel
* no cropped hands, feet, knees, elbows, or head
* consistent lighting, clothing, and body proportions
* athlete wearing simple black athletic clothing and training shoes
* sharp, clean, professional fitness coaching style

### Important restrictions

* Do not overlap movement phases in the same panel
* Do not use motion blur
* Do not use transparent duplicate bodies
* Do not use ghosted movement trails
* Do not add extra people
* Do not clutter the image
* Do not add logos or watermarks
* Do not make the text too large or messy

### Goal

The image should look like a **professional exercise demo card** that clearly teaches the movement step by step and shows proper form in a beginner-friendly way.

        """
    )
    return prompt


def build_exercise_demo_prompt(exercise: dict) -> str:
    """
    Build a realistic exercise demo prompt using exercise details.
    """
    name = exercise.get("name", "exercise")
    category = exercise.get("category", "general")
    level = exercise.get("level", "beginner")
    demo_focus = exercise.get("demo_focus", "correct posture")
    
    prompt = (
        f"Realistic full-body fitness demonstration photo of a person performing a {name} "
        f"in a clean gym setting. Show {demo_focus}. "
        "No text, no labels, no distorted anatomy, no unsafe form."
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

    Tries the primary model first, then falls back
    to FLUX.1-schnell if the primary is unavailable.

    Args:
        exercise_name: The name of the exercise to illustrate.

    Returns:
        Raw image bytes (PNG/JPEG).

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
            width=512,
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


def generate_exercise_demo_image(exercise: dict) -> dict:
    """
    Safe wrapper for generating an exercise demo image.
    Handles API errors safely and returns a result dictionary.
    """
    name = exercise.get("name")
    prompt = build_exercise_demo_prompt(exercise)
    
    if not name:
        return {
            "success": False,
            "image_url": None,
            "error": "Exercise name is missing.",
            "prompt": prompt
        }
        
    try:
        from src.config.settings import TOGETHER_API_KEY
        if not TOGETHER_API_KEY:
            return {
                "success": False,
                "image_url": None,
                "error": "TOGETHER_API_KEY is not configured.",
                "prompt": prompt
            }
            
        # We use the existing function but we override its prompt by patching or we just let it use the default name prompt.
        # Actually, the existing `generate_exercise_image` calls `build_exercise_image_prompt(exercise_name)`.
        # To use the new `build_exercise_demo_prompt`, let's just make the Together API call directly here to ensure it uses `prompt`.
        
        client = Together(api_key=TOGETHER_API_KEY)
        
        try:
            response = client.images.generate(
                prompt=prompt,
                model=IMAGE_MODEL_PRIMARY,
                n=1,
            )
            img_bytes = _extract_image_bytes(response)
        except Exception:
            # Fallback
            response = client.images.generate(
                prompt=prompt,
                model=IMAGE_MODEL_FALLBACK,
                width=512,
                height=512,
                steps=4,
                n=1,
            )
            img_bytes = _extract_image_bytes(response)
            
        # Convert bytes to base64 data URI
        import base64
        b64_str = base64.b64encode(img_bytes).decode('utf-8')
        image_url = f"data:image/png;base64,{b64_str}"
        
        return {
            "success": True,
            "image_url": image_url,
            "error": None,
            "prompt": prompt
        }
    except Exception as e:
        return {
            "success": False,
            "image_url": None,
            "error": str(e),
            "prompt": prompt
        }

