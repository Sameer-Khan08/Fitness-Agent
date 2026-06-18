"""
nutrition_agent.py
------------------
Exposes rule-based nutrition guidance and Together AI nutrition explanation functions.
"""

import json

try:
    from src.nutrition.nutrition_engine import estimate_nutrition_targets
except ImportError:
    estimate_nutrition_targets = None

try:
    from src.agents.together_client import generate_together_text
except ImportError:
    generate_together_text = None


def generate_nutrition_guidance(profile: dict) -> dict:
    """
    Generate rule-based nutrition guidance.
    This should work even if Together AI is unavailable.
    """
    if estimate_nutrition_targets is None:
        return {
            "maintenance_calories": None,
            "target_calories": None,
            "protein_range_g": "Could not estimate protein range.",
            "hydration": "Drink water regularly throughout the day.",
            "meal_structure": [
                "Eat protein with each main meal.",
                "Include fruits or vegetables daily.",
                "Use mostly whole foods.",
                "Avoid extreme dieting."
            ],
            "notes": [
                "Nutrition engine was not available, so this is fallback guidance."
            ],
            "warnings": [
                "This is general fitness guidance only, not a medical diet plan."
            ],
        }

    try:
        return estimate_nutrition_targets(profile)
    except Exception:
        # If the nutrition engine call fails, return safe fallback nutrition guidance
        return {
            "maintenance_calories": None,
            "target_calories": None,
            "protein_range_g": "Could not estimate protein range.",
            "hydration": "Drink water regularly throughout the day.",
            "meal_structure": [
                "Eat protein with each main meal.",
                "Include fruits or vegetables daily.",
                "Use mostly whole foods.",
                "Avoid extreme dieting."
            ],
            "notes": [
                "Nutrition engine call failed, so this is fallback guidance."
            ],
            "warnings": [
                "This is general fitness guidance only, not a medical diet plan."
            ],
        }


def generate_nutrition_ai_explanation(
    nutrition: dict | None = None,
    profile: dict | None = None,
) -> str:
    """
    Generate an AI explanation for nutrition guidance using Together AI.
    The AI only explains the rule-based nutrition result.
    """
    # Robustly handle if arguments are swapped or passed as (profile, nutrition)
    if nutrition and not profile:
        if "main_goal" in nutrition or "gender" in nutrition or "age" in nutrition:
            profile = nutrition
            nutrition = None
    elif nutrition and profile:
        is_first_profile = "main_goal" in nutrition or "gender" in nutrition or "age" in nutrition
        is_second_nutrition = "maintenance_calories" in profile or "protein_range_g" in profile
        if is_first_profile or is_second_nutrition:
            nutrition, profile = profile, nutrition

    nutrition = nutrition or {}
    profile = profile or {}

    system_prompt = """
You provide general nutrition education for fitness goals.

You do not diagnose medical conditions.
You do not prescribe medical diets.
You do not treat eating disorders.
You do not recommend extreme calorie cuts.
Users with medical conditions should consult a doctor or registered dietitian.
Keep the explanation simple, practical, and safe.
"""

    user_prompt = f"""
Explain this nutrition guidance to the user.

User profile:
{json.dumps(profile, indent=2, default=str)}

Nutrition result:
{json.dumps(nutrition, indent=2, default=str)}

Use these headings:

Nutrition Reality Check
Calories
Protein
Hydration
Simple Meal Structure
Warnings
"""

    fallback = f"""
## Nutrition Reality Check

This is general fitness nutrition guidance only. It is not a medical diet plan.

## Calories

Estimated maintenance calories: {nutrition.get("maintenance_calories", "Not available")}

Target calories: {nutrition.get("target_calories", "Not available")}

## Protein

Protein target: {nutrition.get("protein_range_g", "Not available")}

## Hydration

{nutrition.get("hydration", "Drink water regularly throughout the day.")}

## Simple Meal Structure

{chr(10).join("- " + item for item in nutrition.get("meal_structure", ["Eat balanced meals with protein, carbs, fats, fruits, and vegetables."]))}

## Warnings

{chr(10).join("- " + item for item in nutrition.get("warnings", ["Avoid extreme dieting. Consult a qualified professional for medical conditions."]))}
"""

    if generate_together_text is None:
        return fallback

    try:
        return generate_together_text(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            temperature=0.4,
            max_tokens=900,
        )
    except Exception as e:
        return fallback + f"\n\nAI nutrition explanation failed safely: {str(e)}"
