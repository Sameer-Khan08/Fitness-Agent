"""
plan_routes.py
--------------
Routing and handlers for exercise plans, results display, and AI explanation generation.
"""

from flask import render_template, redirect, url_for, session
from src.web.routes import web_bp
from src.agents.fitness_agent import generate_fitness_plan, generate_ai_plan_explanation
from src.config.settings import TEXT_AI_ENABLED, IMAGE_AI_ENABLED
from src.exercises.image_prompts import build_exercise_demo_prompt
from src.memory.image_cache import get_cached_image
from src.web.services import (
    get_profile,
    get_results,
    set_results,
    get_generated_image_count,
    flash_success,
    flash_warning,
    flash_error,
)


@web_bp.route("/plan")
def plan():
    """Render the plan generation configuration preview page."""
    profile = get_profile()
    if not profile:
        flash_warning("Please complete profile setup first.")
        return redirect(url_for("web.onboarding"))
    return render_template("plan.html", profile=profile)


@web_bp.route("/generate-plan", methods=["POST"])
def generate_plan():
    """Trigger the rule-based fitness plan builder and store in session."""
    profile = get_profile()
    if not profile:
        flash_warning("No profile found. Complete profile setup first.")
        return redirect(url_for("web.onboarding"))

    try:
        results = generate_fitness_plan(profile)
        if not results or not results.get("weekly_plan"):
            flash_warning("Plan generation failed. Please check your profile and try again.")
            return redirect(url_for("web.plan"))

        set_results(results)
        session["ai_explanation"] = None
        session.modified = True
        return redirect(url_for("web.results"))

    except Exception as e:
        flash_error(f"Plan generation failed: {str(e)}")
        return redirect(url_for("web.plan"))


@web_bp.route("/results")
def results():
    """Display the generated workout plan and exercise visual cards."""
    results_data = get_results()
    profile = get_profile()

    if not results_data:
        flash_warning("No active plan found. Generate a plan first.")
        return redirect(url_for("web.plan"))

    image_limit_reached = get_generated_image_count() >= 5
    exercise_prompts = {}
    weekly = results_data.get("weekly_plan", [])
    for day_idx, day_plan in enumerate(weekly):
        for ex_idx, exercise in enumerate(day_plan.get("exercises", [])):
            exercise_prompts[f"{day_idx}_{ex_idx}"] = build_exercise_demo_prompt(exercise)

    return render_template(
        "results.html",
        profile=profile,
        plan=results_data,
        results=results_data,
        ai_explanation=session.get("ai_explanation"),
        text_ai_available=bool(TEXT_AI_ENABLED),
        images_available=bool(IMAGE_AI_ENABLED),
        image_limit_reached=image_limit_reached,
        generated_image_count=get_generated_image_count(),
        exercise_prompts=exercise_prompts,
        get_cached_image=get_cached_image,
    )


@web_bp.route("/generate-ai-explanation", methods=["POST"])
def generate_ai_explanation():
    """Call the AI Coach agent to obtain explanation text for the active plan."""
    plan_data = get_results()
    if not plan_data:
        flash_warning("No plan to explain. Generate a plan first.")
        return redirect(url_for("web.plan"))

    explanation = generate_ai_plan_explanation(plan_data)
    session["ai_explanation"] = explanation
    session.modified = True

    from src.config.settings import DESIGN_MODE
    if DESIGN_MODE:
        flash_success("AI coach explanation generated in Design Mode.")
    else:
        flash_success("AI coach explanation generated.")

    return redirect(url_for("web.results"))
