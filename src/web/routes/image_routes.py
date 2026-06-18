"""
image_routes.py
---------------
Routing and handlers for generating exercise demo visuals.
"""

from flask import request, redirect, url_for
from src.web.routes import web_bp
from src.exercises.image_prompts import generate_exercise_demo_image
from src.memory.image_cache import get_cached_image, save_cached_image
from src.config.settings import IMAGE_AI_ENABLED, DESIGN_MODE
from src.web.services import (
    get_results,
    get_generated_image_count,
    increment_generated_image_count,
    flash_warning,
    flash_error,
    flash_info,
    flash_success,
)


@web_bp.route("/generate-exercise-image", methods=["POST"])
def generate_exercise_image_route():
    """Request DALL-E/Together image generation for a particular workout day exercise."""
    plan = get_results()
    if not plan:
        flash_warning("No plan found.")
        return redirect(url_for("web.results"))

    try:
        day_idx = int(request.form.get("day_idx", 0))
        ex_idx = int(request.form.get("ex_idx", 0))
    except (TypeError, ValueError):
        flash_error("Invalid exercise reference.")
        return redirect(url_for("web.results"))

    if DESIGN_MODE:
        flash_info("Exercise image generation is disabled in design mode.")
        return redirect(url_for("web.results") + f"#exercise-{day_idx}-{ex_idx}")

    weekly = plan.get("weekly_plan", [])
    if day_idx < 0 or day_idx >= len(weekly):
        flash_error("Workout day not found.")
        return redirect(url_for("web.results"))

    exercises = weekly[day_idx].get("exercises", [])
    if ex_idx < 0 or ex_idx >= len(exercises):
        flash_error("Exercise not found.")
        return redirect(url_for("web.results"))

    exercise = exercises[ex_idx]
    exercise_name = exercise.get("name", "Exercise")
    force_regenerate = request.form.get("force_regenerate") == "1"

    cached = get_cached_image(exercise_name)
    if cached and cached.get("image_url") and not force_regenerate:
        return redirect(url_for("web.results") + f"#exercise-{day_idx}-{ex_idx}")

    if not IMAGE_AI_ENABLED:
        flash_warning("Exercise image generation is unavailable. Add TOGETHER_API_KEY to enable it.")
        return redirect(url_for("web.results") + f"#exercise-{day_idx}-{ex_idx}")

    count = get_generated_image_count()
    if count >= 5:
        flash_warning("Image generation limit reached for this session.")
        return redirect(url_for("web.results") + f"#exercise-{day_idx}-{ex_idx}")

    result = generate_exercise_demo_image(exercise, force_regenerate=force_regenerate)
    if result.get("success") and result.get("image_url"):
        save_cached_image(exercise_name, result["image_url"], result["prompt"])
        increment_generated_image_count()
        flash_success("Exercise visual generated successfully.")
    else:
        err_msg = result.get("error") or "Unknown error occurred"
        flash_error(f"Image generation failed: {err_msg}")

    return redirect(url_for("web.results") + f"#exercise-{day_idx}-{ex_idx}")
