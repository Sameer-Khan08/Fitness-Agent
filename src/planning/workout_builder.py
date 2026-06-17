"""
workout_builder.py
------------------
Main planning engine that generates a structured, rule-based weekly plan
by combining safety screenings, goal priorities, sport demands, and exercise catalog.
"""

import re
from src.exercises.exercise_library import EXERCISES
from src.safety.medical_flags import detect_medical_red_flags
from src.safety.injury_rules import classify_training_status
from src.planning.goal_engine import get_goal_priorities
from src.planning.sport_engine import get_sport_demands


def matches_avoidance(ex: dict, injuries_lower: str, avoid_list: list[str]) -> bool:
    """
    Check if an exercise matches any injury areas or safety avoidance rules.
    """
    # 1. Check avoid_if tags against injury text and avoid list
    for body_part in ex.get("avoid_if", []):
        bp = body_part.lower()
        if bp in injuries_lower:
            return True
        for aw in avoid_list:
            if bp in aw.lower():
                return True
                
    # 2. Check risk_tags against injury text and avoid list
    for rt in ex.get("risk_tags", []):
        tag = rt.lower()
        if tag in injuries_lower:
            return True
        for aw in avoid_list:
            if tag in aw.lower():
                return True
                
    # 3. Check exercise name against avoid list
    name_lower = ex.get("name", "").lower()
    for aw in avoid_list:
        aw_lower = aw.lower()
        if aw_lower in name_lower or name_lower in aw_lower:
            return True
            
    return False


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

    # 4. Parse session duration into integer minutes
    dur_str = str(profile.get("session_duration", "60"))
    digits = re.findall(r"\d+", dur_str)
    duration_minutes = int(digits[0]) if digits else 60

    # 5. Filter and score exercises based on safety status, injury, level, goal & sport
    avoid_list = safety.get("avoid", [])
    injuries_lower = (profile.get("injuries", "") or "").lower()
    fitness_level = (profile.get("fitness_level", "Beginner")).lower()
    safety_status = safety.get("status", "yellow").lower()

    # Step 5a: Pre-filter by fitness level (Beginner/Intermediate/Advanced)
    level_filtered = []
    for ex in EXERCISES:
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

    # Fallback if level filter leaves too few exercises
    if len(level_filtered) < 3:
        level_filtered = EXERCISES

    # Step 5b: Apply Red/Yellow/Green safety filtering
    safe_exercises = []
    for ex in level_filtered:
        # Check Red Status rules
        if safety_status == "red":
            ex_level = ex.get("level", "beginner").lower()
            # No advanced exercises under red status
            if ex_level == "advanced":
                continue
            # No jumping, sprinting, plyometrics, heavy hinge, intense core
            risk_tags = [r.lower() for r in ex.get("risk_tags", [])]
            if any(tag in risk_tags for tag in ["jumping", "sprinting", "plyometric", "plyometrics", "heavy hinge", "intense core"]):
                continue
            # Avoid matching injury area or restricted pattern
            if matches_avoidance(ex, injuries_lower, avoid_list):
                continue
                
        # Check Yellow Status rules
        elif safety_status == "yellow":
            # Avoid high-risk drills (no jumping, sprinting, plyometrics)
            risk_tags = [r.lower() for r in ex.get("risk_tags", [])]
            if any(tag in risk_tags for tag in ["jumping", "sprinting", "plyometric", "plyometrics"]):
                continue
            # Avoid matching injury area or restricted pattern
            if matches_avoidance(ex, injuries_lower, avoid_list):
                continue
                
        # Check Green Status rules
        else:
            # Even in green status, avoid exercises matching injury area if specified
            if matches_avoidance(ex, injuries_lower, avoid_list):
                continue
                
        safe_exercises.append(ex)

    # Fallback to avoid empty pool
    if not safe_exercises:
        # Fallback to walking or low-impact bike
        safe_exercises = [e for e in EXERCISES if e.get("name") in ["walking", "low-impact bike", "ankle balance drill"]]

    # Step 5c: Score relevance
    goal_name = goal_priorities.get("goal", "general fitness").lower()
    sport_name = sport_demands.get("sport", "none").lower()

    scored_exercises = []
    for ex in safe_exercises:
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

    # 6. Build weekly plan days
    weekly_plan = []

    for d in range(1, days + 1):
        # Determine day parameters
        if safety_status == "red":
            intensity = "low"
            focus = "Restoration, Core & Active Rehab"
            session_type = "Active Recovery & Restoration"
            session_goal = "Promote joint mobility, blood flow, and core stability while protecting healing tissues."
            warm_up = "5 mins very gentle mobility (arm circles, cat-cow, pelvic tilts)"
            cool_down = "5 mins deep breathing and light static stretching"
            coaching_note = "Consult a medical professional if you experience sharp pain. Keep all exercises pain-free."
            # Prioritize mobility, core, and cardio
            day_pool = [e for e in sorted_exercises if e.get("category") in ["mobility", "core", "cardio"]]
            if not day_pool:
                day_pool = sorted_exercises
        elif safety_status == "yellow":
            intensity = "low" if fitness_level == "beginner" else "moderate"
            focus = f"Modified Training & Prehab Focus (Day {d})"
            session_type = "Modified Strength & Prehab"
            session_goal = "Build strength in safe ranges of motion while avoiding restricted movement patterns."
            warm_up = "8-10 mins dynamic warm-up (planks, glute bridges, light mobility)"
            cool_down = "5-10 mins parasympathetic breathing and static stretching"
            coaching_note = "Avoid exercises that trigger discomfort. Substitute with light regressions if needed."
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
                session_type = "Strength & Conditioning"
                session_goal = "Develop structural strength, muscle mass, and power output."
            else:
                focus = f"Sport Readiness & Conditioning (Day {d})"
                session_type = "Conditioning & Sport Readiness"
                session_goal = "Improve cardiovascular capacity, agility, and sport-specific endurance."
                
            warm_up = "10 mins dynamic prep: mobility, muscle activation, and progressive movement prep"
            cool_down = "10 mins static stretching, foam rolling, and deep box breathing"
            coaching_note = "Focus on progressive overload. Keep adding reps or load as form allows."
            day_pool = sorted_exercises

        # Select 5 exercises, offset selections for variety across days
        start_idx = (d - 1) * 3
        day_exercises = []
        
        for i in range(5):  # 5 exercises per day
            pool_idx = (start_idx + i) % len(day_pool)
            base_ex = day_pool[pool_idx]
            
            # Create a full exercise dictionary copy to prevent stripping
            full_ex = base_ex.copy()
            
            # Customize why_you reason
            why_you = f"Selected for {profile.get('main_goal', 'general fitness')} training."
            if safety_status == "red":
                why_you = "Selected as a low-risk option to maintain activity during recovery."
            else:
                # Check goal tags match
                matched_goals = [gt for gt in ex.get("goal_tags", []) if gt in goal_name]
                if matched_goals:
                    why_you = f"Matches your target capacities for {matched_goals[0]}."
                elif profile.get("sport") and profile.get("sport") != "none":
                    why_you = f"Strengthens movement patterns needed for {profile.get('sport')}."
                    
            # Custom coach note making use of demo_focus
            demo_focus = full_ex.get("demo_focus", "proper form")
            coach_note = f"Focus on: {demo_focus}. Keep movements slow and controlled."
            
            full_ex.update({
                "why_you": why_you,
                "coach_note": coach_note
            })
            day_exercises.append(full_ex)
            
        weekly_plan.append({
            "day": f"Day {d}",
            "session_type": session_type,
            "session_goal": session_goal,
            "focus": focus,
            "intensity": intensity,
            "duration_minutes": duration_minutes,
            "warm_up": warm_up,
            "exercises": day_exercises,
            "cool_down": cool_down,
            "coaching_note": coaching_note
        })

    # Add default general coaching notes
    if safety_status == "red":
        notes.append("Focus on recovery and consult with a specialist before increasing load.")
        notes.append("Always prioritize pain-free range of motion. Rest if symptoms flare up.")
    elif safety_status == "yellow":
        notes.append("Avoid training through pain. Adjust sets or reps down if symptoms flare up.")
        notes.append("Use safety regressions and dynamic prehab drills prior to lifting.")
    else:
        notes.append("Ensure progressive overload by adding reps or load when form is stable.")
        notes.append("Maintain high movement quality during conditioning blocks.")

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
