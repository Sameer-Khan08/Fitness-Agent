"""
saved_plan_routes.py
--------------------
Routing and handlers for saving training plans, local dashboards, and past plans logs.
"""

from flask import render_template, redirect, url_for
from src.web.routes import web_bp
from src.memory.plan_store import save_plan_local, get_saved_plans_local, clear_saved_plans_local
from src.web.helpers import get_deployment_checklist
from src.web.services import get_profile, get_results, get_api_status, flash_success, flash_warning, flash_error


@web_bp.route("/save-plan", methods=["POST"])
def save_plan():
    """Archive the active fitness plan to the saved plans collection."""
    plan = get_results()
    profile = get_profile()
    if not plan or not profile:
        flash_warning("No plan to save.")
        return redirect(url_for("web.results"))

    plan_to_save = dict(plan)
    plan_to_save["profile_summary"] = {
        "main_goal": profile.get("main_goal"),
        "sport": profile.get("sport"),
        "fitness_level": profile.get("fitness_level"),
    }
    save_plan_local(plan_to_save)
    flash_success("Plan saved for this session.")
    return redirect(url_for("web.dashboard"))


@web_bp.route("/dashboard")
def dashboard():
    """Render the dashboard overview listing saved programs and application settings checklist."""
    saved_plans = get_saved_plans_local()
    return render_template(
        "dashboard.html",
        saved_plans=saved_plans,
        api_status=get_api_status(),
        checklist=get_deployment_checklist(),
    )


@web_bp.route("/saved-plan/<int:plan_index>")
def saved_plan_detail(plan_index):
    """Retrieve and display specific archived workout plan details."""
    saved_plans = get_saved_plans_local()
    if plan_index < 0 or plan_index >= len(saved_plans):
        flash_error("Saved plan not found.")
        return redirect(url_for("web.dashboard"))
    plan = saved_plans[plan_index]
    return render_template(
        "saved_plan_detail.html",
        plan=plan,
        plan_index=plan_index,
        images_available=False,
        image_limit_reached=True,
        exercise_prompts={},
    )


@web_bp.route("/clear-saved-plans", methods=["POST"])
def clear_saved_plans():
    """Clear all locally stored session plan history logs."""
    clear_saved_plans_local()
    flash_success("Saved plans cleared.")
    return redirect(url_for("web.dashboard"))
