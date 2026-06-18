"""
image_cache.py
--------------
Handles in-memory session caching of generated exercise demonstration images.
"""

import streamlit as st

def get_cached_image(exercise_name: str) -> str | None:
    """
    Retrieve a cached image (data URI or URL) for the given exercise.
    """
    if "image_cache" not in st.session_state:
        st.session_state.image_cache = {}
    return st.session_state.image_cache.get(exercise_name)

def save_cached_image(exercise_name: str, image_url: str) -> None:
    """
    Save the generated image URL to the session cache.
    """
    if "image_cache" not in st.session_state:
        st.session_state.image_cache = {}
    st.session_state.image_cache[exercise_name] = image_url

def clear_image_cache() -> None:
    """
    Clear the cached exercise demonstration images.
    """
    st.session_state.image_cache = {}
