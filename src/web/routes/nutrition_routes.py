"""
nutrition_routes.py
--------------------
Routing for nutrition targets page and AI nutrition guidance.
"""

from flask import render_template, redirect, url_for, session
from src.web.routes import web_bp
from src.nutrition.nutrition_engine import estimate_nutrition_targets
from src.agents.nutrition_agent import generate_nutrition_ai_explanation
from src.config.settings import TEXT_AI_ENABLED
from src.web.services import get_profile, flash_warning, flash_success


@web_bp.route("/nutrition")
def nutrition():
    """Display computed dietary macro-nutrient thresholds based on fitness targets."""
    profile = get_profile()
    if not profile:
        flash_warning("Complete profile setup for nutrition guidance.")
        return redirect(url_for("web.onboarding"))

    nutrition_result = session.get("nutrition_result")
    if not nutrition_result:
        nutrition_result = estimate_nutrition_targets(profile)
        session["nutrition_result"] = nutrition_result
        session.modified = True

    return render_template(
        "nutrition.html",
        profile=profile,
        nutrition=nutrition_result,
        ai_explanation=session.get("nutrition_ai_explanation"),
        text_ai_available=bool(TEXT_AI_ENABLED),
    )


@web_bp.route("/generate-nutrition-ai-explanation", methods=["POST"])
def generate_nutrition_ai_explanation_route():
    """Trigger the AI Coach nutrition explainer module using profile and targets."""
    profile = get_profile()
    if not profile:
        flash_warning("Profile required for nutrition explanation.")
        return redirect(url_for("web.onboarding"))

    nutrition_result = session.get("nutrition_result") or estimate_nutrition_targets(profile)
    session["nutrition_result"] = nutrition_result

    explanation = generate_nutrition_ai_explanation(nutrition=nutrition_result, profile=profile)
    session["nutrition_ai_explanation"] = explanation
    session.modified = True

    from src.config.settings import DESIGN_MODE
    if DESIGN_MODE:
        flash_success("Nutrition AI explanation generated in Design Mode.")
    else:
        flash_success("Nutrition AI explanation generated.")

    return redirect(url_for("web.nutrition"))
