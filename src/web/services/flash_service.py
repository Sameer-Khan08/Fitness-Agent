"""
flash_service.py
----------------
Exposes standard, categorized notification helpers wrapping Flask's flash system.
"""

from flask import flash


def flash_success(message: str) -> None:
    """Flash a success message."""
    flash(message, "success")


def flash_warning(message: str) -> None:
    """Flash a warning message."""
    flash(message, "warning")


def flash_error(message: str) -> None:
    """Flash an error message."""
    flash(message, "error")


def flash_info(message: str) -> None:
    """Flash an info message."""
    flash(message, "info")
