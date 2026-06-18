"""
forms.py
--------
Safe HTML form parsing helpers for Flask routes.
"""


def parse_onboarding_form(form) -> dict:
    """Parse onboarding form data into a profile dictionary."""
    age = form.get("age", "25")
    try:
        age = int(age)
    except (TypeError, ValueError):
        age = 25

    gender = form.get("gender", "Prefer not to say")
    height = form.get("height", "170").strip()
    weight = form.get("weight", "70").strip()
    main_goal = form.get("main_goal", "General Fitness")
    sport = form.get("sport", "None")
    fitness_level = form.get("fitness_level", "Beginner")

    try:
        training_days = int(form.get("training_days_per_week", 3))
    except (TypeError, ValueError):
        training_days = 3
    training_days = max(2, min(7, training_days))

    session_duration = form.get("session_duration", "60 minutes")
    injuries = form.get("injuries", "").strip()
    primary_problem = form.get("primary_problem", "").strip()

    try:
        pain_rating = int(form.get("pain_rating", 0))
    except (TypeError, ValueError):
        pain_rating = 0
    pain_rating = max(0, min(10, pain_rating))

    if not primary_problem:
        primary_problem = f"Goal: {main_goal}. Sport: {sport}. Fitness level: {fitness_level}."

    return {
        "primary_problem": primary_problem,
        "age": age,
        "gender": gender,
        "height_cm": height,
        "weight_kg": weight,
        "main_goal": main_goal,
        "goal": main_goal,
        "sport": sport,
        "main_sport": sport,
        "fitness_level": fitness_level,
        "training_days_per_week": training_days,
        "session_duration": session_duration,
        "injuries": injuries,
        "pain_rating": pain_rating,
    }


def parse_checkin_form(form) -> dict:
    """Parse daily check-in form data."""
    try:
        soreness = int(form.get("soreness", 0))
    except (TypeError, ValueError):
        soreness = 0
    try:
        stress = int(form.get("stress", 0))
    except (TypeError, ValueError):
        stress = 0
    try:
        pain_rating = int(form.get("pain_rating", 0))
    except (TypeError, ValueError):
        pain_rating = 0

    return {
        "sleep_quality": form.get("sleep_quality", "okay"),
        "energy_level": form.get("energy_level", "medium"),
        "soreness": max(0, min(10, soreness)),
        "stress": max(0, min(10, stress)),
        "pain_rating": max(0, min(10, pain_rating)),
        "pain_area": form.get("pain_area", "").strip(),
        "pain_trend": form.get("pain_trend", "same"),
        "trained_yesterday": form.get("trained_yesterday", "no"),
        "ready_to_train": form.get("ready_to_train", "yes"),
    }


DEMO_PROFILES = {
    "athlete": {
        "age": 21,
        "gender": "Male",
        "height_cm": "6'4",
        "weight_kg": "85kg",
        "main_goal": "Athletic Performance",
        "goal": "Athletic Performance",
        "sport": "Football",
        "main_sport": "Football",
        "fitness_level": "Intermediate",
        "training_days_per_week": 4,
        "session_duration": "60 minutes",
        "injuries": "groin pain during sprinting",
        "pain_rating": 5,
        "primary_problem": "Groin pain during sprinting. Football intermediate athlete trying to optimize performance.",
    },
    "weight_loss": {
        "age": 35,
        "gender": "Female",
        "height_cm": "165",
        "weight_kg": "75",
        "main_goal": "Weight Loss",
        "goal": "Weight Loss",
        "sport": "None",
        "main_sport": "None",
        "fitness_level": "Beginner",
        "training_days_per_week": 3,
        "session_duration": "45 minutes",
        "injuries": "",
        "pain_rating": 0,
        "primary_problem": "Weight loss focus, beginner level, no active pain.",
    },
    "groin_pain": {
        "age": 21,
        "gender": "Male",
        "height_cm": "6'4",
        "weight_kg": "85kg",
        "main_goal": "Athletic Performance",
        "goal": "Athletic Performance",
        "sport": "Football",
        "main_sport": "Football",
        "fitness_level": "Intermediate",
        "training_days_per_week": 4,
        "session_duration": "60 minutes",
        "injuries": "groin pain during sprinting",
        "pain_rating": 5,
        "primary_problem": "groin pain during sprinting. Football intermediate athlete.",
    },
    "red_back_pain": {
        "age": 42,
        "gender": "Male",
        "height_cm": "180",
        "weight_kg": "95",
        "main_goal": "Strength",
        "goal": "Strength",
        "sport": "Gym Only",
        "main_sport": "Gym Only",
        "fitness_level": "Advanced",
        "training_days_per_week": 5,
        "session_duration": "75 minutes",
        "injuries": "Lower back pain radiating down leg, numbness in foot",
        "pain_rating": 8,
        "primary_problem": "Lower back pain radiating down leg, numbness in foot. Severe pain, requires safety red flag check.",
    },
}
