"""
components.py
-------------
Shared UI helper components used across multiple pages.
"""

import streamlit as st


def show_medical_disclaimer() -> None:
    """
    Display a standardised medical disclaimer warning in the Streamlit UI.
    This should be shown on any page that involves health or injury data.
    """
    st.warning(
        "⚠️ This tool provides general fitness guidance only. "
        "It is not a medical diagnosis or treatment plan."
    )
