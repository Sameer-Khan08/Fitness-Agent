"""
fitness_agent.py
----------------
Core AI agent for TrainWise AI.

Calls OpenAI GPT-4o-mini with a detailed system prompt and the user's
fitness profile to generate a personalised, injury-aware weekly workout plan.

The plan is returned as a structured Python dictionary parsed from JSON.
"""

import json
import openai

from src.config.settings import OPENAI_API_KEY
from src.planning.goal_engine import get_goal_modifiers
from src.planning.sport_engine import get_sport_context
from src.safety.injury_rules import build_injury_constraints, check_red_flags

# Initialise the OpenAI client with the API key from settings.
client = openai.OpenAI(api_key=OPENAI_API_KEY)

# Model to use for plan generation.
MODEL = "gpt-4o-mini"


# ── System Prompt ────────────────────────────────────────────────────────────

SYSTEM_PROMPT = """
You are TrainWise AI — an elite, evidence-based fitness and athletic performance coach.
You have 20+ years of experience in strength and conditioning, sports science,
injury rehabilitation, and personalised programming.

Your role is to create safe, structured, and highly personalised weekly workout plans
based on each client's profile, goals, fitness level, available training days,
and any reported injuries or pain areas.

You always:
- Prioritise joint health and injury prevention above all else.
- Respect pain and injury constraints absolutely — never programme movements that load
  a painful area without explicit modification.
- Match the complexity and intensity of exercises to the client's fitness level.
- Include warm-up notes, coaching cues, and recovery guidance.
- Provide one practical nutrition tip tailored to the goal.
- Flag any red flag symptoms with a strong recommendation to seek medical advice.

You MUST respond ONLY with a valid JSON object. Do not include any markdown,
code fences, or explanation outside the JSON.

The JSON must follow this exact structure:
{
  "summary": "A 2-3 sentence overview of the plan and its rationale.",
  "weekly_schedule": [
    {
      "day": "Day 1 — e.g. Monday",
      "session_type": "e.g. Full-body Strength",
      "duration_minutes": 60,
      "warm_up": "Brief description of the warm-up (3-5 minutes).",
      "exercises": [
        {
          "name": "Exercise name",
          "sets": 3,
          "reps": "10-12",
          "rest": "60s",
          "notes": "Coaching cue or modification for this client."
        }
      ],
      "cool_down": "Brief cool-down description.",
      "coaching_note": "Session-specific advice or motivation."
    }
  ],
  "injury_notes": "Specific guidance about managing the client's reported injuries during training.",
  "nutrition_tip": "One practical, goal-aligned nutrition tip.",
  "red_flag_warnings": ["List any detected red flags here, or leave as empty array if none."],
  "recovery_advice": "General weekly recovery guidance."
}
""".strip()


# ── User Prompt Builder ──────────────────────────────────────────────────────

def _build_user_prompt(profile: dict, goal_mods: dict, sport_context: str,
                       injury_constraints: str) -> str:
    """
    Build the full user-facing prompt from the client profile and modifiers.
    """
    age = profile.get("age", "unknown")
    gender = profile.get("gender", "not specified")
    height = profile.get("height_cm", "unknown")
    weight = profile.get("weight_kg", "unknown")
    goal = profile.get("main_goal", "General fitness")
    sport = profile.get("sport", "")
    fitness_level = profile.get("fitness_level", "Beginner")
    training_days = profile.get("training_days_per_week", 3)
    session_duration = profile.get("session_duration", "60 minutes")
    injuries = profile.get("injuries", "None reported")
    pain_rating = profile.get("pain_rating", 0)

    sport_line = f"Sport: {sport}" if sport else "Sport: Not applicable"

    prompt = f"""
Please create a personalised weekly workout plan for this client:

--- CLIENT PROFILE ---
Age: {age} years
Gender: {gender}
Height: {height} cm
Weight: {weight} kg
Fitness level: {fitness_level}
Main goal: {goal}
{sport_line}
Training days per week: {training_days}
Preferred session duration: {session_duration}
Reported injuries or pain: {injuries if injuries else "None"}
Pain rating: {pain_rating}/10

--- TRAINING PARAMETERS (based on goal) ---
Rep range: {goal_mods.get("rep_range", "8-12")}
Rest periods: {goal_mods.get("rest_period", "60s")}
Intensity: {goal_mods.get("intensity", "moderate")}
Weekly structure guideline: {goal_mods.get("weekly_structure", "balanced")}
Training focus: {goal_mods.get("focus", "general fitness")}
Avoid: {goal_mods.get("avoid", "nothing specific")}

--- SPORT CONTEXT ---
{sport_context}

--- INJURY AND MOVEMENT CONSTRAINTS ---
{injury_constraints}

--- INSTRUCTIONS ---
- Create exactly {training_days} training sessions spread across the week.
- Each session should fit within {session_duration}.
- Match exercise selection and complexity to a {fitness_level} level.
- Include 4-7 exercises per session (fewer for longer duration, more for shorter circuit-style).
- Provide sets, reps, rest, and coaching notes for every exercise.
- Return only the JSON object. No markdown, no extra text.
""".strip()

    return prompt


# ── Main Plan Generation Function ────────────────────────────────────────────

def generate_plan(profile: dict) -> dict:
    """
    Generate a personalised weekly workout plan for the given user profile.

    Args:
        profile: A dictionary of user fitness data from the onboarding form.

    Returns:
        A structured plan dictionary with weekly schedule, exercises, and advice.

    Raises:
        ValueError:  If the AI returns malformed JSON.
        RuntimeError: If the OpenAI API call fails.
    """
    # Step 1 — Pull goal modifiers and sport context.
    goal = profile.get("main_goal", "General fitness")
    sport = profile.get("sport", "")
    injuries = profile.get("injuries", "")
    pain_rating = profile.get("pain_rating", 0)

    goal_mods = get_goal_modifiers(goal)
    sport_context = get_sport_context(sport)

    # Step 2 — Check red flags and build injury constraints.
    red_flag_warnings = check_red_flags(injuries, pain_rating)
    injury_constraints = build_injury_constraints(injuries, pain_rating)

    # Step 3 — Build prompts.
    user_prompt = _build_user_prompt(profile, goal_mods, sport_context, injury_constraints)

    # Step 4 — Call OpenAI.
    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt},
            ],
            response_format={"type": "json_object"},
            temperature=0.7,
            max_tokens=3000,
        )
    except openai.OpenAIError as e:
        raise RuntimeError(f"OpenAI API error: {e}") from e

    # Step 5 — Parse the JSON response.
    raw_content = response.choices[0].message.content

    try:
        plan = json.loads(raw_content)
    except json.JSONDecodeError as e:
        raise ValueError(f"AI returned invalid JSON: {e}\n\nRaw response:\n{raw_content}") from e

    # Step 6 — Merge any pre-computed red flag warnings with those from the AI.
    existing_warnings = plan.get("red_flag_warnings", [])
    merged_warnings = list(dict.fromkeys(red_flag_warnings + existing_warnings))
    plan["red_flag_warnings"] = merged_warnings

    return plan
