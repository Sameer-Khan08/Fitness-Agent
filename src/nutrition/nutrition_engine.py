"""
nutrition_engine.py
-------------------
Calculates baseline nutrition estimates based on user profile.
Does not provide medical or extreme diet advice.
"""
import re

def parse_weight_kg(weight_str: str) -> float | None:
    if not weight_str:
        return None
    weight_str = str(weight_str).lower().strip()
    match = re.search(r'([\d\.]+)', weight_str)
    if not match:
        return None
    val = float(match.group(1))
    if 'lb' in weight_str or 'lbs' in weight_str:
        return val * 0.453592
    return val

def parse_height_cm(height_str: str) -> float | None:
    if not height_str:
        return None
    height_str = str(height_str).lower().strip()
    # Check for ft/in format like 5'10" or 5ft 10in
    ft_in_match = re.search(r'(\d+)[\'ft\s]+(\d+)?', height_str)
    if ft_in_match and 'cm' not in height_str:
        ft = float(ft_in_match.group(1))
        inches = float(ft_in_match.group(2)) if ft_in_match.group(2) else 0.0
        return (ft * 30.48) + (inches * 2.54)
    
    # Just a number
    match = re.search(r'([\d\.]+)', height_str)
    if not match:
        return None
    val = float(match.group(1))
    if 'm' in height_str and 'cm' not in height_str and val < 3.0:
        return val * 100
    return val

def estimate_nutrition_targets(profile: dict) -> dict:
    """
    Returns simple baseline nutrition guidance.
    """
    goal = str(profile.get("main_goal", "")).lower()
    days = int(profile.get("training_days_per_week", 3))
    gender = str(profile.get("gender", "")).lower()
    age_str = str(profile.get("age", ""))
    
    age = None
    if age_str.isdigit():
        age = int(age_str)
        
    weight_kg = parse_weight_kg(profile.get("weight") or profile.get("weight_kg") or "")
    height_cm = parse_height_cm(profile.get("height") or profile.get("height_cm") or "")
    
    maintenance = None
    target = None
    notes = []
    warnings = [
        "These estimates are approximate and not a medical diet plan.",
        "Users with medical conditions should consult a qualified professional before changing their diet."
    ]
    
    # Estimate Maintenance (Mifflin-St Jeor)
    if weight_kg and height_cm and age and gender in ["male", "m", "female", "f"]:
        if gender in ["male", "m"]:
            bmr = (10 * weight_kg) + (6.25 * height_cm) - (5 * age) + 5
        else:
            bmr = (10 * weight_kg) + (6.25 * height_cm) - (5 * age) - 161
            
        if days <= 2:
            multiplier = 1.375 # light
        elif days <= 4:
            multiplier = 1.55 # moderate
        elif days <= 6:
            multiplier = 1.725 # active
        else:
            multiplier = 1.9 # very active
            
        maintenance = int(bmr * multiplier)
        
        # Determine target
        if "lose" in goal or "weight loss" in goal or "fat loss" in goal:
            target = maintenance - 400
            notes.append("Targeting a modest deficit (approx. 400 calories below maintenance) for sustainable fat loss.")
            warnings.append("Never consume less than 1200 calories (females) or 1500 calories (males) without medical supervision.")
        elif "muscle" in goal or "gain" in goal or "hypertrophy" in goal:
            target = maintenance + 300
            notes.append("Targeting a slight surplus (approx. 300 calories above maintenance) to support muscle growth.")
        else:
            target = maintenance
            notes.append("Targeting maintenance calories to support performance and body composition.")
    else:
        notes.append("Could not calculate exact calorie targets. Please ensure age, gender, height, and weight are entered clearly.")
        
    # Protein Range
    if "lose" in goal or "weight loss" in goal or "fat loss" in goal:
        protein_range_g = "1.6 - 2.2 g per kg of body weight"
        notes.append("Higher protein helps preserve muscle mass while in a calorie deficit.")
    elif "muscle" in goal or "gain" in goal or "strength" in goal:
        protein_range_g = "1.6 - 2.2 g per kg of body weight"
        notes.append("High protein supports muscle repair and hypertrophy.")
    else:
        protein_range_g = "1.2 - 1.6 g per kg of body weight"
        
    hydration = "Aim for at least 3-4 liters (or 1 gallon) of water daily, adding more on training days or in hot climates."
    
    meal_structure = [
        "Base meals around lean protein sources (chicken, fish, tofu, beans).",
        "Include plenty of vegetables for micronutrients and fiber.",
        "Add complex carbohydrates (oats, rice, potatoes) around training windows.",
        "Include healthy fats (nuts, seeds, olive oil, avocado) for hormonal health.",
        "Eat mostly whole, minimally processed foods."
    ]
    
    return {
        "maintenance_calories": maintenance,
        "target_calories": target,
        "protein_range_g": protein_range_g,
        "hydration": hydration,
        "meal_structure": meal_structure,
        "notes": notes,
        "warnings": warnings
    }
