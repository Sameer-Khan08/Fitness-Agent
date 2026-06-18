"""
routes.py
---------
Flask blueprint routes for TrainWise AI web application.
"""

from flask import Blueprint, flash, redirect, render_template, request, session, url_for

from src.agents.fitness_agent import generate_ai_plan_explanation, generate_fitness_plan
from src.agents.nutrition_agent import generate_nutrition_ai_explanation
from src.config.settings import TEXT_AI_ENABLED, IMAGE_AI_ENABLED
from src.exercises.image_prompts import build_exercise_demo_prompt, generate_exercise_demo_image
from src.memory.checkin_store import save_checkin_local
from src.memory.image_cache import get_cached_image, save_cached_image
from src.memory.plan_store import clear_saved_plans_local, get_saved_plans_local, save_plan_local
from src.nutrition.nutrition_engine import estimate_nutrition_targets
from src.planning.readiness_engine import calculate_readiness
from src.planning.workout_adjuster import adjust_workout_for_readiness
from src.web.forms import parse_checkin_form, parse_onboarding_form
from src.web.helpers import (
    clear_current_workflow,
    get_api_status,
    get_current_profile,
    get_current_results,
    get_deployment_checklist,
    has_plan,
    has_profile,
    init_session_defaults,
    set_session_value,
)

web_bp = Blueprint(
    "web",
    __name__,
    template_folder="templates",
    static_folder="static",
)


@web_bp.context_processor
def inject_globals():
    from src.memory.image_cache import get_cached_image
    return {
        "api_status": get_api_status(),
        "get_cached_image": get_cached_image,
    }


@web_bp.before_request
def _ensure_session():
    init_session_defaults()


@web_bp.route("/")
def index():
    if not has_profile():
        return redirect(url_for("web.onboarding"))
    if not has_plan():
        return redirect(url_for("web.plan"))
    return redirect(url_for("web.results"))


@web_bp.route("/onboarding", methods=["GET", "POST"])
def onboarding():
    if request.method == "POST":
        profile = parse_onboarding_form(request.form)
        set_session_value("profile", profile)
        flash("Profile saved. Review your details and generate your plan.", "success")
        return redirect(url_for("web.plan"))
    return render_template("onboarding.html")





@web_bp.route("/plan")
def plan():
    profile = get_current_profile()
    if not profile:
        flash("Please complete profile setup first.", "warning")
        return redirect(url_for("web.onboarding"))
    return render_template("plan.html", profile=profile)


@web_bp.route("/generate-plan", methods=["POST"])
def generate_plan():
    profile = session.get("profile")
    
    print("GENERATE PLAN ROUTE HIT")
    print("PROFILE:", profile)

    if not profile:
        flash("No profile found. Complete profile setup first.", "warning")
        return redirect(url_for("web.onboarding"))

    try:
        results = generate_fitness_plan(profile)
        
        print("RESULT KEYS:", results.keys() if isinstance(results, dict) else type(results))

        if not results or not results.get("weekly_plan"):
            flash("Plan generation failed. Please check your profile and try again.", "warning")
            return redirect(url_for("web.plan"))

        session["results"] = results
        session["ai_explanation"] = None
        session.modified = True

        return redirect(url_for("web.results"))

    except Exception as e:
        flash(f"Plan generation failed: {str(e)}", "error")
        return redirect(url_for("web.plan"))


@web_bp.route("/results")
def results():
    results = session.get("results")
    profile = session.get("profile")

    if not results:
        flash("No active plan found. Generate a plan first.", "warning")
        return redirect(url_for("web.plan"))

    image_limit_reached = session.get("generated_image_count", 0) >= 5
    exercise_prompts = {}
    weekly = results.get("weekly_plan", [])
    for day_idx, day_plan in enumerate(weekly):
        for ex_idx, exercise in enumerate(day_plan.get("exercises", [])):
            exercise_prompts[f"{day_idx}_{ex_idx}"] = build_exercise_demo_prompt(exercise)

    return render_template(
        "results.html",
        profile=profile,
        plan=results,
        results=results,
        ai_explanation=session.get("ai_explanation"),
        text_ai_available=bool(TEXT_AI_ENABLED),
        images_available=bool(IMAGE_AI_ENABLED),
        image_limit_reached=image_limit_reached,
        generated_image_count=session.get("generated_image_count", 0),
        exercise_prompts=exercise_prompts,
        get_cached_image=get_cached_image,
    )


@web_bp.route("/generate-ai-explanation", methods=["POST"])
def generate_ai_explanation():
    plan = get_current_results()
    if not plan:
        flash("No plan to explain. Generate a plan first.", "warning")
        return redirect(url_for("web.plan"))
    if not TEXT_AI_ENABLED:
        flash("AI explanation unavailable: No text AI API key is configured.", "warning")
        return redirect(url_for("web.results"))
    explanation = generate_ai_plan_explanation(plan)
    set_session_value("ai_explanation", explanation)
    flash("AI coach explanation generated.", "success")
    return redirect(url_for("web.results"))


@web_bp.route("/daily-checkin", methods=["GET", "POST"])
def daily_checkin():
    if not has_profile() or not has_plan():
        flash("Generate a fitness plan before daily check-in.", "warning")
        return redirect(url_for("web.plan") if has_profile() else url_for("web.onboarding"))

    if request.method == "POST":
        checkin = parse_checkin_form(request.form)
        save_checkin_local(checkin)
        readiness = calculate_readiness(checkin)
        set_session_value("current_readiness", readiness)

        plan = get_current_results()
        adjusted = None
        if plan and plan.get("weekly_plan"):
            today_workout = plan["weekly_plan"][0]
            adjusted = adjust_workout_for_readiness(today_workout, readiness)
        set_session_value("adjusted_today_workout", adjusted)
        return redirect(url_for("web.daily_result"))

    return render_template("daily_checkin.html")


@web_bp.route("/daily-result")
def daily_result():
    readiness = session.get("current_readiness")
    if not readiness:
        flash("Complete a daily check-in first.", "warning")
        return redirect(url_for("web.daily_checkin"))
    return render_template(
        "daily_result.html",
        readiness=readiness,
        adjusted_workout=session.get("adjusted_today_workout"),
        images_available=bool(IMAGE_AI_ENABLED),
        image_limit_reached=session.get("generated_image_count", 0) >= 5,
        exercise_prompts={},
    )


@web_bp.route("/nutrition")
def nutrition():
    profile = get_current_profile()
    if not profile:
        flash("Complete profile setup for nutrition guidance.", "warning")
        return redirect(url_for("web.onboarding"))

    nutrition_result = session.get("nutrition_result")
    if not nutrition_result:
        nutrition_result = estimate_nutrition_targets(profile)
        set_session_value("nutrition_result", nutrition_result)

    return render_template(
        "nutrition.html",
        profile=profile,
        nutrition=nutrition_result,
        ai_explanation=session.get("nutrition_ai_explanation"),
        text_ai_available=bool(TEXT_AI_ENABLED),
    )


@web_bp.route("/generate-nutrition-ai-explanation", methods=["POST"])
def generate_nutrition_ai_explanation_route():
    profile = get_current_profile()
    if not profile:
        flash("Profile required for nutrition explanation.", "warning")
        return redirect(url_for("web.onboarding"))
    nutrition_result = session.get("nutrition_result") or estimate_nutrition_targets(profile)
    set_session_value("nutrition_result", nutrition_result)
    if not TEXT_AI_ENABLED:
        flash("AI explanation unavailable: No text AI API key is configured.", "warning")
        return redirect(url_for("web.nutrition"))
    explanation = generate_nutrition_ai_explanation(nutrition=nutrition_result, profile=profile)
    set_session_value("nutrition_ai_explanation", explanation)
    flash("Nutrition AI explanation generated.", "success")
    return redirect(url_for("web.nutrition"))


@web_bp.route("/save-plan", methods=["POST"])
def save_plan():
    plan = get_current_results()
    profile = get_current_profile()
    if not plan or not profile:
        flash("No plan to save.", "warning")
        return redirect(url_for("web.results"))
    plan_to_save = dict(plan)
    plan_to_save["profile_summary"] = {
        "main_goal": profile.get("main_goal"),
        "sport": profile.get("sport"),
        "fitness_level": profile.get("fitness_level"),
    }
    save_plan_local(plan_to_save)
    flash("Plan saved for this session.", "success")
    return redirect(url_for("web.dashboard"))


@web_bp.route("/dashboard")
def dashboard():
    saved_plans = get_saved_plans_local()
    return render_template(
        "dashboard.html",
        saved_plans=saved_plans,
        api_status=get_api_status(),
        checklist=get_deployment_checklist(),
    )


@web_bp.route("/saved-plan/<int:plan_index>")
def saved_plan_detail(plan_index):
    saved_plans = get_saved_plans_local()
    if plan_index < 0 or plan_index >= len(saved_plans):
        flash("Saved plan not found.", "error")
        return redirect(url_for("web.dashboard"))
    plan = saved_plans[plan_index]
    return render_template("saved_plan_detail.html", plan=plan, plan_index=plan_index,
                           images_available=False, image_limit_reached=True, exercise_prompts={})


@web_bp.route("/clear-saved-plans", methods=["POST"])
def clear_saved_plans():
    clear_saved_plans_local()
    flash("Saved plans cleared.", "success")
    return redirect(url_for("web.dashboard"))


@web_bp.route("/start-over", methods=["POST"])
def start_over():
    clear_current_workflow()
    flash("Session reset. Start with a new profile.", "success")
    return redirect(url_for("web.onboarding"))


@web_bp.route("/generate-exercise-image", methods=["POST"])
def generate_exercise_image_route():
    plan = get_current_results()
    if not plan:
        flash("No plan found.", "warning")
        return redirect(url_for("web.results"))

    try:
        day_idx = int(request.form.get("day_idx", 0))
        ex_idx = int(request.form.get("ex_idx", 0))
    except (TypeError, ValueError):
        flash("Invalid exercise reference.", "error")
        return redirect(url_for("web.results"))

    weekly = plan.get("weekly_plan", [])
    if day_idx < 0 or day_idx >= len(weekly):
        flash("Workout day not found.", "error")
        return redirect(url_for("web.results"))

    exercises = weekly[day_idx].get("exercises", [])
    if ex_idx < 0 or ex_idx >= len(exercises):
        flash("Exercise not found.", "error")
        return redirect(url_for("web.results"))

    exercise = exercises[ex_idx]
    exercise_name = exercise.get("name", "Exercise")
    force_regenerate = request.form.get("force_regenerate") == "1"

    cached = get_cached_image(exercise_name)
    if cached and cached.get("image_url") and not force_regenerate:
        return redirect(url_for("web.results") + f"#exercise-{day_idx}-{ex_idx}")

    if not IMAGE_AI_ENABLED:
        flash("Exercise image generation is unavailable. Add TOGETHER_API_KEY to enable it.", "warning")
        return redirect(url_for("web.results") + f"#exercise-{day_idx}-{ex_idx}")

    count = session.get("generated_image_count", 0)
    if count >= 5:
        flash("Image generation limit reached for this session.", "warning")
        return redirect(url_for("web.results") + f"#exercise-{day_idx}-{ex_idx}")

    result = generate_exercise_demo_image(exercise, force_regenerate=force_regenerate)
    if result.get("success") and result.get("image_url"):
        save_cached_image(exercise_name, result["image_url"], result["prompt"])
        set_session_value("generated_image_count", count + 1)
        flash("Exercise visual generated successfully.", "success")
    else:
        err_msg = result.get("error") or "Unknown error occurred"
        flash(f"Image generation failed: {err_msg}", "error")

    return redirect(url_for("web.results") + f"#exercise-{day_idx}-{ex_idx}")
