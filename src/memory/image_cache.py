from datetime import datetime
from src.web.helpers import get_session_value, set_session_value


def get_cached_image(exercise_name: str) -> dict | None:
    """Retrieve cached image metadata for the given exercise."""
    cache = get_session_value("image_cache", {})
    if not isinstance(cache, dict):
        cache = {}
    name = exercise_name.lower().strip()
    return cache.get(name)


def save_cached_image(exercise_name: str, image_url: str, prompt: str) -> None:
    """Save the generated image URL and metadata to the session cache."""
    cache = get_session_value("image_cache", {})
    if not isinstance(cache, dict):
        cache = {}
    name = exercise_name.lower().strip()
    cache[name] = {
        "image_url": image_url,
        "prompt": prompt,
        "generated_at": datetime.now().isoformat(),
        "exercise_name": exercise_name
    }
    set_session_value("image_cache", cache)


def clear_image_cache() -> None:
    """Clear cached exercise visual images."""
    set_session_value("image_cache", {})
