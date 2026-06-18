"""
checkin_routes.py
------------------
Routing for daily user readiness check-ins and auto-adjusted workouts.
"""

from flask import render_template, request, redirect, url_for, session
from src.web.routes import web_bp
from src.web.forms import parse_checkin_form
from src.memory.checkin_store import save_checkin_local
from src.planning.readiness_engine import calculate_readiness
from src.planning.workout_adjuster import adjust_workout_for_readiness
from src.config.settings import IMAGE_AI_ENABLED
from src.web.services import (
    get_profile,
    get_results,
    get_generated_image_count,
    flash_warning,
)


@web_bp.route("/daily-checkin", methods=["GET", "POST"])
def daily_checkin():
    """Handle submissions to soreness, sleep, and pain check-ins to compute readiness."""
    if not get_profile() or not get_results():
        flash_warning("Generate a fitness plan before daily check-in.")
        return redirect(url_for("web.plan") if get_profile() else url_for("web.onboarding"))

    if request.method == "POST":
        checkin = parse_checkin_form(request.form)
        save_checkin_local(checkin)
        readiness = calculate_readiness(checkin)
        session["current_readiness"] = readiness

        plan_data = get_results()
        adjusted = None
        if plan_data and plan_data.get("weekly_plan"):
            today_workout = plan_data["weekly_plan"][0]
            adjusted = adjust_workout_for_readiness(today_workout, readiness)
        session["adjusted_today_workout"] = adjusted
        session.modified = True
        return redirect(url_for("web.daily_result"))

    return render_template("daily_checkin.html")


@web_bp.route("/daily-result")
def daily_result():
    """Display computed readiness score and the resulting adjusted workout program for today."""
    readiness = session.get("current_readiness")
    if not readiness:
        flash_warning("Complete a daily check-in first.")
        return redirect(url_for("web.daily_checkin"))

    return render_template(
        "daily_result.html",
        readiness=readiness,
        adjusted_workout=session.get("adjusted_today_workout"),
        images_available=bool(IMAGE_AI_ENABLED),
        image_limit_reached=get_generated_image_count() >= 5,
        exercise_prompts={},
    )
