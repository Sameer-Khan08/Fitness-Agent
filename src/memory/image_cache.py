"""
image_cache.py
--------------
Handles session caching of generated exercise demonstration images.
"""

from src.web.helpers import get_session_value, set_session_value


def get_cached_image(exercise_name: str) -> str | None:
    """Retrieve a cached image (data URI or URL) for the given exercise."""
    cache = get_session_value("image_cache", {})
    if not isinstance(cache, dict):
        cache = {}
    return cache.get(exercise_name)


def save_cached_image(exercise_name: str, image_url: str) -> None:
    """Save the generated image URL to the session cache."""
    cache = get_session_value("image_cache", {})
    if not isinstance(cache, dict):
        cache = {}
    cache[exercise_name] = image_url
    set_session_value("image_cache", cache)


def clear_image_cache() -> None:
    """Clear cached exercise demonstration images."""
    set_session_value("image_cache", {})
