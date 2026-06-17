"""
injury_rules.py
---------------
Contains constants and helper functions for injury screening.
Checks user-reported pain areas and symptoms against red flag lists
before plan generation.
"""

from src.safety.medical_flags import GENERAL_RED_FLAGS

# Common body areas where users may experience pain or injury.
PAIN_AREAS: list[str] = [
    "neck",
    "shoulder",
    "elbow",
    "wrist",
    "lower back",
    "hip",
    "groin",
    "knee",
    "ankle",
    "achilles",
    "foot",
]

# Pain rating threshold at or above which extra warnings are triggered.
HIGH_PAIN_THRESHOLD = 8


def check_red_flags(injuries: str, pain_rating: int) -> list[str]:
    """
    Scan user-reported injuries for red flag symptoms and high pain ratings.

    Args:
        injuries:    Free-text injury description entered by the user.
        pain_rating: Numeric pain rating from 0 to 10.

    Returns:
        A list of warning strings. Empty list means no red flags detected.
    """
    warnings = []

    if not injuries:
        injuries = ""

    injuries_lower = injuries.lower()

    # Check for any red flag keywords in the injury description.
    for flag in GENERAL_RED_FLAGS:
        if flag in injuries_lower:
            warnings.append(
                f"⚠️ Red flag symptom detected: '{flag}'. "
                "Please consult a doctor or physiotherapist before starting any exercise program."
            )

    # Check for high pain rating.
    if pain_rating >= HIGH_PAIN_THRESHOLD:
        warnings.append(
            f"⚠️ High pain rating reported ({pain_rating}/10). "
            "Training with pain at this level is not recommended. "
            "Please seek medical advice before exercising."
        )

    return warnings


def build_injury_constraints(injuries: str, pain_rating: int) -> str:
    """
    Build a plain-text constraint string to inject into the AI prompt.
    Tells the AI what to avoid or modify based on reported injuries.

    Args:
        injuries:    Free-text injury description.
        pain_rating: Numeric pain rating from 0 to 10.

    Returns:
        A string of injury constraints for the AI prompt.
    """
    if not injuries or injuries.strip() == "":
        return "The user has reported no injuries or pain. No movement restrictions apply."

    pain_label = "low" if pain_rating <= 3 else "moderate" if pain_rating <= 6 else "high"

    return (
        f"The user has reported the following injuries or pain areas: '{injuries}'. "
        f"Current pain rating: {pain_rating}/10 ({pain_label}). "
        "You MUST: "
        "(1) Avoid any exercises that load or stress the reported pain areas through full range, "
        "(2) Suggest appropriate modifications or regressions for affected movements, "
        "(3) Include relevant mobility and stability work to support recovery, "
        "(4) Flag any sessions where the user should monitor symptoms carefully."
    )
