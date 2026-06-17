"""
goal_engine.py
--------------
Maps user fitness goals to training parameter modifiers.
These modifiers shape the AI prompt to bias the plan
toward the correct style of training.
"""

# Mapping of user goals to training focus descriptors.
# Each entry guides the AI on volume, intensity, rest, and priorities.
GOAL_MODIFIERS: dict[str, dict] = {
    "Weight loss": {
        "rep_range": "12–20",
        "rest_period": "30–45 seconds",
        "intensity": "moderate",
        "weekly_structure": "3–4 days strength, 2 days cardio/conditioning",
        "focus": (
            "metabolic conditioning, compound movements, superset-friendly circuits, "
            "caloric burn, and moderate-intensity cardio"
        ),
        "avoid": "heavy 1RM work, extreme fatigue without cardio component",
    },
    "Muscle gain": {
        "rep_range": "6–12",
        "rest_period": "60–90 seconds",
        "intensity": "moderate-high",
        "weekly_structure": "4–5 days strength, progressive overload focus",
        "focus": (
            "hypertrophy, progressive overload, compound lifts as primary movers, "
            "isolation finishers, and adequate recovery"
        ),
        "avoid": "excessive cardio, very high reps with light weight",
    },
    "General fitness": {
        "rep_range": "8–15",
        "rest_period": "45–60 seconds",
        "intensity": "moderate",
        "weekly_structure": "balanced mix of strength and conditioning",
        "focus": (
            "balanced full-body development, functional movement patterns, "
            "aerobic base, and lifestyle fitness"
        ),
        "avoid": "extreme specialisation in one direction",
    },
    "Athletic development": {
        "rep_range": "3–8 (power) + 10–15 (conditioning)",
        "rest_period": "90–120 seconds for power sets, 30–45 for conditioning",
        "intensity": "high",
        "weekly_structure": "periodised — power days + conditioning days",
        "focus": (
            "explosive power, speed, agility, plyometrics, reactive strength, "
            "and sport-relevant movement patterns"
        ),
        "avoid": "slow grinding rep tempos, excessive isolation work",
    },
    "Sport-specific training": {
        "rep_range": "varies by block",
        "rest_period": "varies by block",
        "intensity": "moderate-high",
        "weekly_structure": "sport-aligned periodisation",
        "focus": (
            "movement patterns and energy systems specific to the athlete's sport, "
            "injury prevention, and performance transfer"
        ),
        "avoid": "generic bodybuilding routines unrelated to sport demands",
    },
    "Injury rehabilitation": {
        "rep_range": "15–20 (low load)",
        "rest_period": "60–90 seconds",
        "intensity": "low-moderate",
        "weekly_structure": "3–4 days low-load progressive loading",
        "focus": (
            "joint stability, mobility restoration, neuromuscular control, "
            "gradual progressive loading, and pain-free range of motion"
        ),
        "avoid": (
            "loaded movements through pain, ballistic or plyometric exercises, "
            "heavy compound lifts near injured area"
        ),
    },
    "Improve endurance": {
        "rep_range": "15–25 (strength), long duration cardio",
        "rest_period": "30–60 seconds",
        "intensity": "low-moderate (aerobic base) + tempo intervals",
        "weekly_structure": "2 strength days + 3–4 cardio/conditioning days",
        "focus": (
            "aerobic base building (Zone 2), lactate threshold work, "
            "tempo runs or cycles, and supporting strength for efficiency"
        ),
        "avoid": "heavy maximal lifts, excessive DOMS that impairs cardio sessions",
    },
}


def get_goal_modifiers(goal: str) -> dict:
    """
    Return training parameter modifiers for the given goal.

    Args:
        goal: The user's main fitness goal string.

    Returns:
        A dict of training modifiers, or a general fitness default if unknown.
    """
    return GOAL_MODIFIERS.get(goal, GOAL_MODIFIERS["General fitness"])
