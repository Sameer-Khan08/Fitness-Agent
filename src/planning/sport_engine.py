"""
sport_engine.py
---------------
Maps user sports to demands and prehab focuses.
Supports rule-based lookup for MVP plan builders.
"""

# Mapping of sports to demands and prehab focus
SPORT_DEMANDS_MAP: dict[str, dict] = {
    "football": {
        "demands": ["acceleration", "deceleration", "change of direction", "repeated sprints", "aerobic fitness"],
        "prehab_focus": ["groin", "hamstrings", "calves", "ankles", "knees"],
    },
    "soccer": {
        "demands": ["acceleration", "deceleration", "change of direction", "repeated sprints", "aerobic fitness"],
        "prehab_focus": ["groin", "hamstrings", "calves", "ankles", "knees"],
    },
    "basketball": {
        "demands": ["jumping", "landing", "lateral movement", "acceleration", "deceleration"],
        "prehab_focus": ["knees", "ankles", "calves", "hips"],
    },
    "cricket": {
        "demands": ["sprinting", "rotational power", "shoulder durability", "core strength"],
        "prehab_focus": ["shoulders", "lower back", "hamstrings"],
    },
    "tennis": {
        "demands": ["lateral movement", "reaction speed", "shoulder endurance", "footwork"],
        "prehab_focus": ["shoulders", "knees", "ankles", "wrists"],
    },
    "badminton": {
        "demands": ["lateral movement", "reaction speed", "shoulder endurance", "footwork"],
        "prehab_focus": ["shoulders", "knees", "ankles", "wrists"],
    },
    "running": {
        "demands": ["running economy", "aerobic endurance", "ankle stability", "calf endurance"],
        "prehab_focus": ["calves", "achilles", "knees", "hips"],
    },
    "gym only": {
        "demands": ["strength progression", "hypertrophy patterns", "joint stabilization", "range of motion"],
        "prehab_focus": ["shoulders", "wrists", "lower back", "hips"],
    },
    "none": {
        "demands": ["general agility", "core power", "aerobic base", "multi-planar strength"],
        "prehab_focus": ["knees", "shoulders", "lower back", "ankles"],
    }
}


def get_sport_demands(sport: str) -> dict:
    """
    Get the rule-based demands and prehab focus for the user's sport.

    Args:
        sport: The sport name string.

    Returns:
        A dictionary with keys: sport, demands, prehab_focus.
    """
    if not sport:
        sport = "none"
        
    sport_key = sport.strip().lower()

    matched = SPORT_DEMANDS_MAP.get(sport_key)
    if not matched:
        # Partial match
        for key, value in SPORT_DEMANDS_MAP.items():
            if key in sport_key or sport_key in key:
                matched = value
                sport_key = key
                break
        else:
            # Fallback
            matched = SPORT_DEMANDS_MAP["none"]
            sport_key = "general athletic demands"

    return {
        "sport": sport_key,
        "demands": matched["demands"],
        "prehab_focus": matched["prehab_focus"]
    }


# Keep the legacy modifiers if referenced elsewhere in results_page, etc.
SPORT_CONTEXTS: dict[str, str] = {
    "football": "Football demands explosive acceleration, deceleration, multi-directional speed, lower-body power, and high aerobic capacity.",
    "soccer": "Soccer requires sustained aerobic endurance, explosive sprinting, lateral agility, and lower-body strength.",
    "basketball": "Basketball demands vertical power, lateral quickness, upper-body strength for contact, and high-intensity conditioning.",
    "tennis": "Tennis requires rotational power, shoulder health, lateral movement, wrist stability, and aerobic-anaerobic conditioning.",
    "badminton": "Badminton requires agility, hand-eye coordination, quick lunges, overhead striking capacity, and rapid footwork.",
    "running": "Running requires cardiorespiratory volume, repeated loading capacity, calf resilience, and hamstring/quad balanced power.",
    "gym only": "Gym training requires balanced lifting volume, form awareness, progressive resistance, and core stabilization.",
    "none": "Build a well-rounded athletic plan appropriate for general physical preparation.",
}


def get_sport_context(sport: str) -> str:
    """
    Legacy context builder.
    """
    if not sport:
        return SPORT_CONTEXTS["none"]
    sport_key = sport.strip().lower()
    if sport_key in SPORT_CONTEXTS:
        return SPORT_CONTEXTS[sport_key]
    for key, context in SPORT_CONTEXTS.items():
        if key in sport_key or sport_key in key:
            return context
    return f"Physical prep focused on sport demands for: {sport}."
