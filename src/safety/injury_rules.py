"""
injury_rules.py
---------------
Contains constants and helper functions for classifying training status
and generating injury-specific avoidance rules.
"""

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


def classify_training_status(profile: dict) -> dict:
    """
    Classify training status (green, yellow, red) based on the user profile pain rating,
    and generate custom avoidances and recommendations.

    Args:
        profile: The user profile dictionary.

    Returns:
        A dictionary with keys: status, summary, avoid, recommendations.
    """
    pain_rating = profile.get("pain_rating")
    
    # If pain rating is missing, default to yellow.
    if pain_rating is None:
        status = "yellow"
    elif pain_rating <= 3:
        status = "green"
    elif pain_rating <= 6:
        status = "yellow"
    else:
        status = "red"

    avoid = []
    recommendations = []
    
    # Base summaries, avoids, and recommendations based on status
    if status == "green":
        summary = "User can train normally but should still warm up and progress gradually."
        recommendations.append("Begin each session with dynamic warm-up drills.")
        recommendations.append("Progress training volume and intensity gradually week-over-week.")
    elif status == "yellow":
        summary = "User can train, but should modify intensity and avoid painful movements."
        recommendations.append("Cap intensity at a moderate level.")
        recommendations.append("Swap any movements that trigger pain with pain-free regressions.")
    else:  # red
        summary = "User should avoid intense training and seek professional help if pain is severe, worsening, sharp, or limiting movement."
        recommendations.append("Focus on low-intensity mobility, stability, and restoration work.")
        recommendations.append("Consult a doctor or physiotherapist for diagnostic evaluation.")

    # Area-specific avoid rules based on injury text
    injury_text = (profile.get("injuries", "") or "").lower()

    if "groin" in injury_text:
        avoid.extend(["sprinting", "hard cutting", "aggressive adductor stretching"])
        recommendations.append("Focus on closed-chain hip stability and core work.")

    if "knee" in injury_text:
        avoid.extend(["high-volume jumping", "deep painful squats", "hard deceleration drills"])
        recommendations.append("Prioritize hip-dominant exercises (e.g. glute bridges) to offload the knee joint.")

    if "ankle" in injury_text or "achilles" in injury_text:
        avoid.extend(["max sprinting", "plyometrics", "hard change of direction"])
        recommendations.append("Prioritize calf raises and ankle balance/stability drills.")

    if "shoulder" in injury_text:
        avoid.extend(["painful overhead pressing", "heavy dips", "unstable heavy pressing"])
        recommendations.append("Focus on rotator cuff strengthening and horizontal pulling patterns.")

    if "lower back" in injury_text:
        avoid.extend(["heavy deadlifts", "heavy squats", "loaded spinal flexion"])
        recommendations.append("Focus on neutral-spine core stabilization (e.g. dead bugs, planks) and hip mobility.")

    if "wrist" in injury_text or "elbow" in injury_text:
        avoid.extend(["painful curls", "heavy gripping", "painful push-ups"])
        recommendations.append("Use neutral grip (dumbbells) where possible and avoid high-grip-strength demands.")

    return {
        "status": status,
        "summary": summary,
        "avoid": avoid,
        "recommendations": recommendations,
    }
