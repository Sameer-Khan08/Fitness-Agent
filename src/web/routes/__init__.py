"""
routes package initialization.
Declares the web blueprint and registers all sub-route modules.
"""

from flask import Blueprint
from src.web.services import init_session_defaults, get_api_status

web_bp = Blueprint(
    "web",
    __name__,
)


@web_bp.context_processor
def inject_globals():
    """Inject global context helpers into Jinja templates."""
    from src.memory.image_cache import get_cached_image
    from src.config.settings import DESIGN_MODE
    return {
        "api_status": get_api_status(),
        "get_cached_image": get_cached_image,
        "DESIGN_MODE": DESIGN_MODE,
    }


@web_bp.before_request
def _ensure_session():
    """Ensure Flask session variables are initialized before handling requests."""
    init_session_defaults()


# Import route handlers to register them on the blueprint.
# Imported at the end to prevent circular dependency issues.
from src.web.routes import main_routes
from src.web.routes import profile_routes
from src.web.routes import plan_routes
from src.web.routes import checkin_routes
from src.web.routes import nutrition_routes
from src.web.routes import image_routes
from src.web.routes import saved_plan_routes
