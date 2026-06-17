"""
fitness_agent.py
----------------
Agent wrapper for TrainWise AI.
Currently configured to run fully local and rule-based for the MVP stage.
"""

from src.planning.workout_builder import build_weekly_plan


def generate_fitness_plan(profile: dict) -> dict:
    """
    Generate a rule-based training plan by invoking the local planning engine.

    Args:
        profile: The user profile dictionary.

    Returns:
        A structured training plan dictionary.
    """
    return build_weekly_plan(profile)


def generate_plan(profile: dict) -> dict:
    """
    Legacy wrapper function that routes to the local rule-based engine.
    Ensures complete rule-based compatibility across existing page setups.
    """
    return generate_fitness_plan(profile)


def generate_ai_plan_explanation(plan: dict) -> str:
    """
    Generate an AI coach explanation for the rule-based fitness plan.
    Falls back to a simple string if OPENAI_API_KEY is not configured.
    """
    from src.config.settings import OPENAI_API_KEY
    import json
    
    if not OPENAI_API_KEY:
        return "AI explanation is unavailable because OPENAI_API_KEY is missing. Please follow the rule-based plan instructions carefully."

    import openai
    
    client = openai.OpenAI(api_key=OPENAI_API_KEY)
    
    system_prompt = (
        "You are a fitness and athletic performance assistant.\n"
        "You provide general fitness education only.\n"
        "You do not diagnose injuries.\n"
        "You do not replace a doctor, physiotherapist, or qualified coach.\n"
        "You must respect the rule-based safety status provided.\n"
        "You must not tell a red-status user to train hard.\n"
        "You must keep warnings clear.\n"
        "You must explain in simple language.\n\n"
        "Return a concise explanation with exactly these headings (use markdown h3):\n"
        "### Reality Check\n"
        "### Why This Plan Fits You\n"
        "### What To Avoid\n"
        "### How To Use The Plan\n"
        "### When To Seek Professional Help"
    )
    
    user_prompt = f"Please explain the following generated training plan:\n{json.dumps(plan, indent=2)}"
    
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.7,
            max_tokens=800
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Could not generate AI explanation. Error: {str(e)}"
