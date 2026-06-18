"""
profile_routes.py
------------------
Onboarding and profile creation routing for TrainWise AI.
"""

from flask import render_template, request, redirect, url_for
from src.web.routes import web_bp
from src.web.forms import parse_profile_form
from src.web.services import set_profile, flash_success


@web_bp.route("/onboarding", methods=["GET", "POST"])
def onboarding():
    """Render profile questionnaire or save completed onboarding profile data."""
    if request.method == "POST":
        profile = parse_profile_form(request.form)
        set_profile(profile)
        flash_success("Profile saved. Review your details and generate your plan.")
        return redirect(url_for("web.plan"))
    return render_template("onboarding.html")
