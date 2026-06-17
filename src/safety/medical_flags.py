"""
medical_flags.py
----------------
Contains constant lists of general red flag symptoms and functions to check them.
These are warning signs that may indicate a serious medical condition.
"""

# Symptoms that should prompt the user to stop and seek medical advice.
GENERAL_RED_FLAGS: list[str] = [
    "chest pain",
    "fainting",
    "dizziness",
    "severe shortness of breath",
    "numbness",
    "tingling",
    "loss of strength",
    "severe swelling",
    "pain above 7 out of 10",
    "pain at rest",
    "night pain",
    "sudden sharp pain",
    "unable to walk normally",
]


def detect_medical_red_flags(profile: dict) -> dict:
    """
    Check the user's profile for medical red flags based on pain rating
    and reported injuries or symptoms.

    Args:
        profile: The user profile dictionary.

    Returns:
        A dictionary with keys: has_red_flags, flags, message.
    """
    flags = []
    pain_rating = profile.get("pain_rating", 0)
    injuries_text = profile.get("injuries", "") or ""
    injuries_lower = injuries_text.lower()

    # Rule 1: Pain rating of 8 or above
    if pain_rating >= 8:
        flags.append("Pain is very high.")

    # Rule 2: Search for red flag keywords/phrases in injury description
    for flag in GENERAL_RED_FLAGS:
        if flag in injuries_lower:
            flags.append(f"Matching red flag symptom: '{flag}'")

    has_red_flags = len(flags) > 0
    message = ""

    if has_red_flags:
        message = (
            "🚨 Medical Red Flag Detected: Based on your reported symptoms or pain level, "
            "it is strongly recommended that you stop intense training and consult a qualified "
            "doctor or physiotherapist before commencing any training program."
        )
    else:
        message = "No critical medical red flags detected."

    return {
        "has_red_flags": has_red_flags,
        "flags": flags,
        "message": message
    }
