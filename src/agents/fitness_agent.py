import json

from src.planning.workout_builder import build_weekly_plan

try:
    from src.agents.together_client import generate_together_text
except Exception:
    generate_together_text = None


def generate_fitness_plan(profile: dict) -> dict:
    """
    Generate the main rule-based fitness plan.
    This is the core planner used by routes.py.
    """
    return build_weekly_plan(profile)


def generate_ai_plan_explanation(plan: dict) -> str:
    """
    Generate an AI coach explanation for an already-created rule-based plan.
    The AI only explains the plan. It must not replace or override safety logic.
    """

    if not plan:
        return "No plan was found to explain. Generate a training plan first."

    safety = plan.get("safety", {})
    medical = plan.get("medical", {})
    goal_priorities = plan.get("goal_priorities", {})
    sport_demands = plan.get("sport_demands", {})
    weekly_plan = plan.get("weekly_plan", [])

    avoid = safety.get("avoid", [])

    system_prompt = """
You are an AI fitness and athletic performance coach.

You provide general fitness education only.
You do not diagnose injuries.
You do not replace a doctor, physiotherapist, or qualified coach.
You must respect the rule-based safety status provided by the app.
You must not tell a red-status user to train hard.
You must keep medical warnings clear and simple.
Use simple, practical language.
"""

    user_prompt = f"""
Explain this fitness plan to the user.

Rule-based safety status:
{safety.get("status", "unknown")}

Safety summary:
{safety.get("summary", "")}

Medical red flags:
{medical.get("flags", [])}

Medical message:
{medical.get("message", "")}

What to avoid:
{avoid}

Goal priorities:
{json.dumps(goal_priorities, indent=2, default=str)}

Sport demands:
{json.dumps(sport_demands, indent=2, default=str)}

Weekly plan:
{json.dumps(weekly_plan, indent=2, default=str)}

Return the explanation with these headings:

Reality Check
Why This Plan Fits You
What To Avoid
How To Use The Plan
When To Seek Professional Help
"""

    fallback = f"""
## Reality Check

Your current safety status is **{safety.get("status", "unknown")}**.

{safety.get("summary", "Follow the rule-based plan carefully.")}

## Why This Plan Fits You

This plan was generated from your goal, sport, fitness level, pain rating, and injury information.

## What To Avoid

Avoid: {", ".join(avoid) if avoid else "No specific avoid list was found."}

## How To Use The Plan

Follow the weekly plan gradually. Warm up before training, use controlled form, and stop any movement that increases pain.

## When To Seek Professional Help

{medical.get("message", "If pain is severe, worsening, sharp, or limiting movement, consult a qualified doctor or physiotherapist.")}
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
        return fallback + f"\n\nAI explanation failed safely: {str(e)}"