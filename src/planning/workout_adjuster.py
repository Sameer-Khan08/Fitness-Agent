"""
workout_adjuster.py
-------------------
Adjusts a generated workout day based on daily readiness.
"""

import copy

def adjust_workout_for_readiness(workout_day: dict, readiness: dict) -> dict:
    """
    Safely adjusts a daily workout plan based on the calculated readiness status.
    Returns a modified copy of the workout_day.
    """
    if not workout_day:
        return workout_day
        
    adjusted = copy.deepcopy(workout_day)
    status = readiness.get("readiness", "green")
    
    if status == "green":
        adjusted["coaching_note"] = "Readiness is optimal. Train as prescribed."
        return adjusted
        
    elif status == "yellow":
        adjusted["intensity"] = "low/moderate"
        adjusted["coaching_note"] = "Readiness is compromised. Intensity reduced and high-risk movements removed."
        
        # Remove high-risk exercises
        safe_exercises = []
        for ex in adjusted.get("exercises", []):
            risk_tags = [t.lower() for t in ex.get("risk_tags", [])]
            name = ex.get("name", "").lower()
            if any(t in risk_tags for t in ["jumping", "sprinting", "plyometric", "plyometrics", "heavy hinge"]):
                continue
            if "jump" in name or "sprint" in name:
                continue
            safe_exercises.append(ex)
            
        adjusted["exercises"] = safe_exercises
        
    elif status == "red":
        adjusted["intensity"] = "low"
        adjusted["session_type"] = "Active Recovery"
        adjusted["coaching_note"] = "⚠️ RED READINESS. Do not perform intense training. Consult a professional if pain is severe."
        adjusted["exercises"] = [
            {
                "name": "Walking or Low-Impact Bike",
                "sets": "1",
                "reps": "15-20 minutes",
                "instructions": ["Keep heart rate very low.", "Focus on gentle movement."],
                "risk_tags": []
            },
            {
                "name": "Gentle Mobility",
                "sets": "1",
                "reps": "5-10 minutes",
                "instructions": ["Slow, controlled stretching.", "Avoid pushing into pain."],
                "risk_tags": []
            },
            {
                "name": "Glute Bridge & Dead Bug",
                "sets": "2",
                "reps": "10",
                "instructions": ["Gentle core and hip activation.", "Stop if painful."],
                "risk_tags": []
            }
        ]
        
    return adjusted
