"""
workout_builder.py
------------------
Main planning engine that generates a structured, rule-based weekly plan
by combining safety screenings, goal priorities, sport demands, and exercise catalog.
"""

from src.exercises.exercise_library import EXERCISES
from src.safety.medical_flags import detect_medical_red_flags
from src.safety.injury_rules import classify_training_status
from src.planning.goal_engine import get_goal_priorities
from src.planning.sport_engine import get_sport_demands


def build_weekly_plan(profile: dict) -> dict:
    """
    Generate a rule-based training program customized to the user's profile.

    Args:
        profile: The user profile dictionary containing age, goal, pain, sport, etc.

    Returns:
        A dictionary with keys: profile_summary, safety, medical, goal_priorities,
        sport_demands, weekly_plan, notes.
    """
    notes = []
    pain_rating = profile.get("pain_rating", 0)

    # 1. Run safety checks and medical screen
    medical = detect_medical_red_flags(profile)
    safety = classify_training_status(profile)

    # 2. Retrieve goal priorities & sport demands
    goal_priorities = get_goal_priorities(profile.get("main_goal", "general fitness"))
    sport_demands = get_sport_demands(profile.get("sport", "none"))

    # 3. Schedule days bounding (Min 2, Max 6)
    days_input = profile.get("training_days_per_week", 3)
    if days_input < 2:
        days = 2
        notes.append("Minimum training frequency is 2 days/week. Plan has been adjusted to 2 days.")
    elif days_input > 6:
        days = 6
        notes.append("Maximum training frequency is 6 days/week. Plan has been capped at 6 days to guarantee recovery.")
    else:
        days = days_input

    # 4. Filter and score exercises based on safety status, injury, level, goal & sport
    avoid_list = safety.get("avoid", [])
    injuries_lower = (profile.get("injuries", "") or "").lower()
    fitness_level = (profile.get("fitness_level", "Beginner")).lower()

    # Step 4a: Injury avoidance filter
    safe_exercises = []
    for ex in EXERCISES:
        should_avoid = False
        
        # Check if the exercise contains any avoid tags matching user pain areas
        for body_part in ex.get("avoid_if", []):
            if body_part in injuries_lower:
                should_avoid = True
                break
            for aw in avoid_list:
                if body_part in aw.lower():
                    should_avoid = True
                    break
        
        if not should_avoid:
            safe_exercises.append(ex)

    # Step 4b: Fitness level filter
    level_filtered = []
    for ex in safe_exercises:
        ex_level = ex.get("level", "beginner").lower()
        if fitness_level == "beginner":
            # Beginner only gets beginner exercises
            if ex_level == "beginner":
                level_filtered.append(ex)
        elif fitness_level == "intermediate":
            # Intermediate gets beginner & intermediate
            if ex_level in ["beginner", "intermediate"]:
                level_filtered.append(ex)
        else:
            # Advanced gets all levels
            level_filtered.append(ex)

    # Fallback: if level filter leaves too few exercises (< 5), fallback to all safe ones
    if len(level_filtered) < 5:
        level_filtered = safe_exercises

    # Step 4c: Score relevance
    goal_name = goal_priorities.get("goal", "general fitness").lower()
    sport_name = sport_demands.get("sport", "none").lower()

    scored_exercises = []
    for ex in level_filtered:
        score = 0
        
        # Match goal tags
        for gt in ex.get("goal_tags", []):
            if gt in goal_name:
                score += 3
                
        # Match sport tags
        for st in ex.get("sport_tags", []):
            if st in sport_name:
                score += 2
                
        scored_exercises.append((score, ex))

    # Sort by score descending
    scored_exercises.sort(key=lambda x: x[0], reverse=True)
    sorted_exercises = [item[1] for item in scored_exercises]

    # 5. Build weekly plan days
    weekly_plan = []
    safety_status = safety.get("status", "yellow")

    for d in range(1, days + 1):
        # Determine day parameters
        if safety_status == "red":
            intensity = "low"
            focus = "Restoration, Core & Active Rehab"
            # Prioritize mobility, core, and cardio
            day_pool = [e for e in sorted_exercises if e.get("category") in ["mobility", "core", "cardio"]]
            if not day_pool:
                day_pool = sorted_exercises
        elif safety_status == "yellow":
            intensity = "low" if fitness_level == "beginner" else "moderate"
            focus = f"Modified Training & Prehab Focus (Day {d})"
            # Mix prehab, strength, and core
            day_pool = sorted_exercises
        else:  # green
            if fitness_level == "beginner":
                intensity = "moderate"
            elif fitness_level == "intermediate":
                intensity = "moderate" if d % 2 == 0 else "high"
            else:
                intensity = "high"
            
            # Alternate focus styles
            if d % 2 == 1:
                focus = f"{goal_priorities.get('training_style', 'Balanced').title()} (Day {d})"
            else:
                focus = f"Sport Readiness & Conditioning (Day {d})"
            day_pool = sorted_exercises

        # Select 4-6 exercises, offset selections for variety across days
        start_idx = (d - 1) * 3
        day_exercises = []
        
        # Loop through pool wrapping index
        for i in range(5):  # default to 5 exercises per day
            pool_idx = (start_idx + i) % len(day_pool)
            base_ex = day_pool[pool_idx]
            
            # Format exercise dict for weekly plan output format
            day_exercises.append({
                "name": base_ex.get("name"),
                "sets": base_ex.get("sets", "3"),
                "reps": base_ex.get("reps", "10"),
                "why_you": f"Selected for {profile.get('main_goal', 'general fitness')} training.",
                "notes": base_ex.get("instructions", ["Perform under control."])[0]
            })
            
        weekly_plan.append({
            "day": f"Day {d}",
            "focus": focus,
            "intensity": intensity,
            "exercises": day_exercises
        })

    # Add default general coaching notes
    if safety_status == "red":
        notes.append("Focus on recovery and consult with a specialist before increasing load.")
    elif safety_status == "yellow":
        notes.append("Avoid training through pain. Adjust sets or reps down if symptoms flare up.")
    else:
        notes.append("Ensure progressive overload by adding reps or load when form is stable.")

    # Package profile summary
    profile_summary = {
        "age": profile.get("age"),
        "gender": profile.get("gender"),
        "height": profile.get("height_cm"),
        "weight": profile.get("weight_kg"),
        "main_goal": profile.get("main_goal"),
        "sport": profile.get("sport"),
        "fitness_level": profile.get("fitness_level"),
        "training_days_per_week": days,
        "session_duration": profile.get("session_duration", "60 minutes"),
        "injuries": profile.get("injuries"),
        "pain_rating": pain_rating,
    }

    return {
        "profile_summary": profile_summary,
        "safety": safety,
        "medical": medical,
        "goal_priorities": goal_priorities,
        "sport_demands": sport_demands,
        "weekly_plan": weekly_plan,
        "notes": notes
    }
