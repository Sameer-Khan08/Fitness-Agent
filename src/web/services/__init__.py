"""
Services package initialization.
Exposes Flask session management, flash categorized warnings, and API connection status checkers.
"""

from src.web.services.session_interface import MemorySessionInterface
from src.web.services.session_service import (
    init_session_defaults,
    get_profile,
    set_profile,
    clear_profile,
    get_results,
    set_results,
    clear_results,
    get_saved_plans,
    set_saved_plans,
    get_image_cache,
    set_image_cache,
    get_generated_image_count,
    increment_generated_image_count,
    clear_current_workflow,
)
from src.web.services.flash_service import (
    flash_success,
    flash_warning,
    flash_error,
    flash_info,
)
from src.web.services.api_status_service import get_api_status

__all__ = [
    "MemorySessionInterface",
    "init_session_defaults",
    "get_profile",
    "set_profile",
    "clear_profile",
    "get_results",
    "set_results",
    "clear_results",
    "get_saved_plans",
    "set_saved_plans",
    "get_image_cache",
    "set_image_cache",
    "get_generated_image_count",
    "increment_generated_image_count",
    "clear_current_workflow",
    "flash_success",
    "flash_warning",
    "flash_error",
    "flash_info",
    "get_api_status",
]
