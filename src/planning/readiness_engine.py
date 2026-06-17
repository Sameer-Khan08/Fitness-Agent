"""
readiness_engine.py
-------------------
Calculates daily readiness score based on user check-in data.
"""

def calculate_readiness(checkin: dict, profile: dict | None = None) -> dict:
    """
    Calculate a daily readiness score and status based on check-in parameters.
    """
    score = 100
    
    sleep_quality = checkin.get("sleep_quality", "okay")
    energy_level = checkin.get("energy_level", "medium")
    soreness = int(checkin.get("soreness", 0))
    stress = int(checkin.get("stress", 0))
    pain_rating = int(checkin.get("pain_rating", 0))
    pain_trend = checkin.get("pain_trend", "same")
    
    # Deductions
    if sleep_quality == "poor":
        score -= 15
    elif sleep_quality == "good":
        score += 5
        
    if energy_level == "low":
        score -= 15
    elif energy_level == "high":
        score += 5
        
    score -= (soreness * 2)
    score -= (stress * 1)
    score -= (pain_rating * 5)
    
    if pain_trend == "worse":
        score -= 20
        
    score = max(0, min(100, score))
    
    readiness = "green"
    avoid_today = []
    modifications = []
    
    if pain_rating >= 8:
        readiness = "red"
        recommendation = "Recovery Only - Please consult a professional."
        modifications.append("Cancel high-intensity training.")
        avoid_today.append("Any loaded movement or high-impact exercise.")
    elif pain_rating >= 4 or pain_trend == "worse" or score < 50:
        readiness = "yellow" if readiness != "red" else "red"
        if score < 30:
            readiness = "red"
        
    if readiness == "green":
        if score < 70:
            readiness = "yellow"

    if readiness == "green":
        summary = "You are fully recovered and ready to train."
        recommendation = "Train Normally"
    elif readiness == "yellow":
        summary = "Your recovery is compromised or you are experiencing mild pain."
        recommendation = "Modify Training"
        modifications.append("Reduce intensity and load by 20-30%.")
        modifications.append("Extend warm-up duration.")
        avoid_today.append("High-risk exercises (jumping, heavy hinging, plyometrics)")
        if soreness >= 7:
            avoid_today.append("Exercises targeting highly sore areas")
    else:  # red
        summary = "Critical warning signs detected (high pain or very low recovery)."
        recommendation = "Recovery Only"
        modifications.append("Skip main workout and focus on active recovery.")
        avoid_today.append("All intense training")
        
    return {
        "readiness": readiness,
        "score": score,
        "summary": summary,
        "recommendation": recommendation,
        "avoid_today": avoid_today,
        "modifications": modifications
    }
