"""
image_cache.py
--------------
Handles caching of generated exercise demo images during the session.
"""

import streamlit as st

def get_cached_image(exercise_name: str) -> str | None:
    """Retrieve an image URL or base64 string from the cache by exercise name."""
    if "image_cache" not in st.session_state:
        st.session_state.image_cache = {}
    return st.session_state.image_cache.get(exercise_name)

def save_cached_image(exercise_name: str, image_url: str) -> None:
    """Save an image to the cache for the given exercise name."""
    if "image_cache" not in st.session_state:
        st.session_state.image_cache = {}
    if exercise_name:
        st.session_state.image_cache[exercise_name] = image_url

def clear_image_cache() -> None:
    """Clear all images from the cache."""
    st.session_state.image_cache = {}
