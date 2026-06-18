"""
main_routes.py
--------------
Main entry points and session reset routing for TrainWise AI.
"""

from flask import redirect, url_for
from src.web.routes import web_bp
from src.web.services import (
    get_profile,
    get_results,
    clear_current_workflow,
    flash_success,
)


@web_bp.route("/")
def index():
    """Redirect user based on current profile and plan generation state."""
    if not get_profile():
        return redirect(url_for("web.onboarding"))
    if not get_results():
        return redirect(url_for("web.plan"))
    return redirect(url_for("web.results"))


@web_bp.route("/start-over", methods=["POST"])
def start_over():
    """Clear session-specific workflow data and start profile setup again."""
    clear_current_workflow()
    flash_success("Session reset. Start with a new profile.")
    return redirect(url_for("web.onboarding"))
