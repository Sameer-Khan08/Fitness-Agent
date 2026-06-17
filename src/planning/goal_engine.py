"""
goal_engine.py
--------------
Maps user fitness goals to training parameter modifiers and priorities.
Supports rule-based lookup for MVP plan builders.
"""

# Mapping of goals to priorities and training style.
GOAL_PRIORITIES_MAP: dict[str, dict] = {
    "weight loss": {
        "priorities": ["full-body strength", "low-impact cardio", "daily walking", "nutrition consistency"],
        "training_style": "metabolic & strength balance",
    },
    "muscle gain": {
        "priorities": ["progressive overload", "hypertrophy training", "protein intake", "recovery"],
        "training_style": "hypertrophy focus",
    },
    "general fitness": {
        "priorities": ["full-body strength", "cardiovascular fitness", "core stability", "functional mobility"],
        "training_style": "balanced physical preparedness",
    },
    "athletic performance": {
        "priorities": ["strength", "mobility", "power", "conditioning", "injury prevention"],
        "training_style": "athletic conditioning & power",
    },
    "sport-specific performance": {
        "priorities": ["strength transfer", "speed/agility", "conditioning", "mobility", "prehab"],
        "training_style": "sport transfer phase",
    },
    "strength": {
        "priorities": ["compound lifting strength", "neuromuscular power", "progressive tension", "rest intervals"],
        "training_style": "heavy strength focus",
    },
    "endurance": {
        "priorities": ["cardiorespiratory volume", "pacing efficiency", "muscular stamina", "aerobic capacity"],
        "training_style": "aerobic conditioning focus",
    },
    "mobility": {
        "priorities": ["joint range of motion", "flexibility maintenance", "postural control", "stiffness relief"],
        "training_style": "active mobility & recovery",
    },
}


def get_goal_priorities(goal: str) -> dict:
    """
    Get the rule-based priorities and training style for the user's fitness goal.

    Args:
        goal: The goal string.

    Returns:
        A dictionary with keys: goal, priorities, training_style.
    """
    if not goal:
        goal = ""
    
    goal_key = goal.strip().lower()

    # Match exact key or default to general fitness
    matched = GOAL_PRIORITIES_MAP.get(goal_key)
    if not matched:
        # Try a partial check
        for key, value in GOAL_PRIORITIES_MAP.items():
            if key in goal_key or goal_key in key:
                matched = value
                goal_key = key
                break
        else:
            # Fallback
            matched = GOAL_PRIORITIES_MAP["general fitness"]
            goal_key = "general fitness"

    return {
        "goal": goal_key,
        "priorities": matched["priorities"],
        "training_style": matched["training_style"]
    }


# Keep the legacy modifiers if referenced elsewhere in results_page, etc.
GOAL_MODIFIERS: dict[str, dict] = {
    "Weight loss": {
        "rep_range": "12–20",
        "rest_period": "30–45 seconds",
        "intensity": "moderate",
        "weekly_structure": "3–4 days strength, 2 days cardio/conditioning",
        "focus": "metabolic conditioning, compound movements, superset-friendly circuits, caloric burn, and moderate-intensity cardio",
        "avoid": "heavy 1RM work, extreme fatigue without cardio component",
    },
    "Muscle gain": {
        "rep_range": "6–12",
        "rest_period": "60–90 seconds",
        "intensity": "moderate-high",
        "weekly_structure": "4–5 days strength, progressive overload focus",
        "focus": "hypertrophy, progressive overload, compound lifts as primary movers, isolation finishers, and adequate recovery",
        "avoid": "excessive cardio, very high reps with light weight",
    },
    "General fitness": {
        "rep_range": "8–15",
        "rest_period": "45–60 seconds",
        "intensity": "moderate",
        "weekly_structure": "balanced mix of strength and conditioning",
        "focus": "balanced full-body development, functional movement patterns, aerobic base, and lifestyle fitness",
        "avoid": "extreme specialisation in one direction",
    },
    "Athletic development": {
        "rep_range": "3–8 (power) + 10–15 (conditioning)",
        "rest_period": "90–120 seconds for power sets, 30–45 for conditioning",
        "intensity": "high",
        "weekly_structure": "periodised — power days + conditioning days",
        "focus": "explosive power, speed, agility, plyometrics, reactive strength, and sport-relevant movement patterns",
        "avoid": "slow grinding rep tempos, excessive isolation work",
    },
    "Sport-specific training": {
        "rep_range": "varies by block",
        "rest_period": "varies by block",
        "intensity": "moderate-high",
        "weekly_structure": "sport-aligned periodisation",
        "focus": "movement patterns and energy systems specific to the athlete's sport, injury prevention, and performance transfer",
        "avoid": "generic bodybuilding routines unrelated to sport demands",
    },
    "Injury rehabilitation": {
        "rep_range": "15–20 (low load)",
        "rest_period": "60–90 seconds",
        "intensity": "low-moderate",
        "weekly_structure": "3–4 days low-load progressive loading",
        "focus": "joint stability, mobility restoration, neuromuscular control, gradual progressive loading, and pain-free range of motion",
        "avoid": "loaded movements through pain, ballistic or plyometric exercises, heavy compound lifts near injured area",
    },
    "Improve endurance": {
        "rep_range": "15–25 (strength), long duration cardio",
        "rest_period": "30–60 seconds",
        "intensity": "low-moderate (aerobic base) + tempo intervals",
        "weekly_structure": "2 strength days + 3–4 cardio/conditioning days",
        "focus": "aerobic base building (Zone 2), lactate threshold work, tempo runs or cycles, and supporting strength for efficiency",
        "avoid": "heavy maximal lifts, excessive DOMS that impairs cardio sessions",
    },
}


def get_goal_modifiers(goal: str) -> dict:
    """
    Legacy modifier mapping.
    """
    # Try case insensitive match or standard key match
    if not goal:
        return GOAL_MODIFIERS["General fitness"]
    for key in GOAL_MODIFIERS.keys():
        if key.lower() == goal.strip().lower():
            return GOAL_MODIFIERS[key]
    return GOAL_MODIFIERS["General fitness"]
