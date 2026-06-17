"""
sport_engine.py
---------------
Maps a user's sport to movement priorities and relevant context.
This context is injected into the AI prompt to personalise the plan
toward the physical demands of that sport.
"""

# Sport → training context mapping.
# Each entry describes the key physical demands and movement patterns
# the AI should emphasise when building a sport-specific plan.
SPORT_CONTEXTS: dict[str, str] = {
    "football": (
        "Football demands explosive acceleration, deceleration, multi-directional speed, "
        "lower-body power, and high aerobic capacity. Prioritise sprint mechanics, "
        "change-of-direction drills, lower-body plyometrics, and repeated sprint ability."
    ),
    "soccer": (
        "Soccer requires sustained aerobic endurance, explosive sprinting, lateral agility, "
        "and lower-body strength. Include hamstring and groin prehab, plyometrics, and aerobic base work."
    ),
    "basketball": (
        "Basketball demands vertical power, lateral quickness, upper-body strength for contact, "
        "and high-intensity intermittent conditioning. Prioritise jump training, ankle stability, "
        "reactive agility, and court conditioning."
    ),
    "tennis": (
        "Tennis requires rotational power, shoulder health, lateral movement, wrist stability, "
        "and aerobic-anaerobic conditioning. Include thoracic rotation, shoulder cuff work, "
        "split-step drills, and short-burst interval conditioning."
    ),
    "swimming": (
        "Swimming demands lat and shoulder strength, thoracic rotation, hip flexibility, "
        "and aerobic capacity. Prioritise overhead shoulder stability, lat pull patterns, "
        "core anti-rotation, and breathing mechanics."
    ),
    "rugby": (
        "Rugby needs full-body strength and power, tackling resilience, sprinting, "
        "and high aerobic capacity. Include heavy compound lifts, collision preparation, "
        "sprint work, and conditioning circuits."
    ),
    "cricket": (
        "Cricket requires rotational power for batting and bowling, shoulder health, "
        "core stability, and repeated sprint ability. Include thoracic rotation, shoulder prehab, "
        "lateral movement patterns, and sprint conditioning."
    ),
    "running": (
        "Running performance is built on aerobic base, running economy, hip and glute strength, "
        "and calf/achilles resilience. Prioritise Zone 2 aerobic running, hip extension strength, "
        "single-leg stability, and progressive mileage loading."
    ),
    "cycling": (
        "Cycling demands quad and glute endurance, hip flexor mobility, core stability, "
        "and aerobic capacity. Include posterior chain work to balance quad dominance, "
        "hip mobility, and aerobic threshold training."
    ),
    "martial arts": (
        "Martial arts require explosive power, rotational strength, anaerobic conditioning, "
        "and flexibility. Include rotational power work, posterior chain strength, "
        "plyometrics, and high-intensity interval conditioning."
    ),
    "golf": (
        "Golf demands thoracic rotation, hip mobility, glute strength, shoulder stability, "
        "and core anti-rotation control. Include rotational mobility drills, glute activation, "
        "and single-leg balance work."
    ),
    "gymnastics": (
        "Gymnastics needs bodyweight strength, shoulder and wrist stability, flexibility, "
        "and spatial awareness. Prioritise overhead pressing stability, active flexibility, "
        "core control, and bodyweight strength progressions."
    ),
    "weightlifting": (
        "Olympic weightlifting demands explosive hip extension, overhead stability, "
        "ankle and thoracic mobility, and neuromuscular coordination. "
        "Include pulling patterns, overhead stability work, and mobility for receiving positions."
    ),
    "crossfit": (
        "CrossFit combines strength, gymnastics, and metabolic conditioning. "
        "Include Olympic lift technique work, gymnastic progressions, and "
        "high-intensity conditioning circuits."
    ),
}

DEFAULT_SPORT_CONTEXT = (
    "No specific sport was provided. Build a well-rounded athletic plan "
    "appropriate for the user's stated goal and fitness level."
)


def get_sport_context(sport: str) -> str:
    """
    Return the sport-specific training context string.

    Args:
        sport: The user's sport as entered in the onboarding form.

    Returns:
        A descriptive string of sport demands and training priorities.
    """
    if not sport or sport.strip() == "":
        return DEFAULT_SPORT_CONTEXT

    sport_key = sport.strip().lower()

    # Direct match
    if sport_key in SPORT_CONTEXTS:
        return SPORT_CONTEXTS[sport_key]

    # Partial match — check if sport name appears in any key
    for key, context in SPORT_CONTEXTS.items():
        if key in sport_key or sport_key in key:
            return context

    # No match found — return a generic context with the sport name
    return (
        f"The user plays {sport}. Design the plan to complement the physical demands "
        f"of this sport, considering relevant movement patterns, energy systems, "
        f"and injury prevention for athletes in this discipline."
    )
