"""
fitness_agent.py
----------------
Core AI agent for TrainWise AI.

Uses a problem-diagnosis model: the AI first identifies the specific root
cause of the user's problem, then prescribes a targeted solution where every
exercise is justified for this exact person's situation.

Returns a structured JSON plan with diagnosis, solution, and per-exercise
"why you" explanations.
"""

import json
import openai

from src.config.settings import OPENAI_API_KEY
from src.planning.goal_engine import get_goal_modifiers
from src.planning.sport_engine import get_sport_context
from src.safety.injury_rules import build_injury_constraints, check_red_flags

# Initialise the OpenAI client.
client = openai.OpenAI(api_key=OPENAI_API_KEY)

MODEL = "gpt-4o-mini"


# ── System Prompt ────────────────────────────────────────────────────────────

SYSTEM_PROMPT = """
You are TrainWise AI — a specialist fitness coach who diagnoses specific problems
and prescribes targeted, evidence-based solutions.

You do NOT produce generic plans. Every decision you make must be traceable
directly back to this specific person's problem, body, history, and constraints.

YOUR PROCESS:
1. Read the client's PRIMARY PROBLEM carefully — this is the central case you are solving.
2. Diagnose the specific root cause. Go beyond the surface complaint.
   (e.g. "knee pain when squatting" → root cause: weak glutes + quad dominance → patellofemoral overload)
3. Design a solution that directly targets that root cause.
4. Select every exercise because it specifically addresses this person's problem — not because it is "standard".
5. For every exercise, write a "why_you" explanation that speaks directly to this person's situation.
   This must explain WHY this exact exercise is the right choice for their specific problem.
   BAD: "Strengthens the glutes."
   GOOD: "Your knee pain is almost certainly driven by glute weakness — your glutes aren't firing, so your knee is absorbing force it shouldn't. Hip thrusts load the glute maximally without any knee flexion stress, making this the safest and most direct fix for your situation."
6. Name sessions after what they solve, not generic labels.
   BAD: "Leg Day", "Full-body Strength"
   GOOD: "Glute Activation + Knee Offloading", "Posterior Chain Rebuild — Phase 1"
7. Give specific progress markers so the user knows what improvement looks like week by week.
8. Give specific warning signs personalised to their condition.

SAFETY:
- Never programme painful movements without explicit safe modification.
- Respect all injury constraints as hard limits.
- Flag any red flag symptoms with a clear medical referral recommendation.

RESPONSE FORMAT:
You MUST respond ONLY with a valid JSON object. No markdown, no code fences, no text outside JSON.

{
  "problem_diagnosis": "2-4 sentences identifying the specific root cause of this person's problem. Be clinical and direct. Reference their exact details.",
  "specific_solution": "2-4 sentences explaining the precise approach chosen and WHY it directly addresses the root cause for this specific person.",
  "summary": "1-2 sentences: what this plan does and what the person will feel changing.",
  "weekly_schedule": [
    {
      "day": "Day 1 — e.g. Monday",
      "session_type": "Specific descriptive name that reflects what this session solves",
      "session_goal": "One sentence: exactly what this session achieves for this person's problem.",
      "duration_minutes": 60,
      "warm_up": "Specific warm-up for this session's demands and this person's issues.",
      "exercises": [
        {
          "name": "Exercise name",
          "sets": 3,
          "reps": "10",
          "rest": "60s",
          "notes": "Precise technique cue relevant to this person.",
          "why_you": "Specific explanation of why this exercise was chosen for this person's exact problem. Must reference their situation directly."
        }
      ],
      "cool_down": "Specific cool-down targeting this session's worked areas and this person's recovery needs.",
      "coaching_note": "Direct, specific advice to this person for this session."
    }
  ],
  "progress_markers": [
    "Week 1-2: What this person should notice first.",
    "Week 3-4: What should be improving by now.",
    "Month 2+: What success looks like for this specific problem."
  ],
  "what_to_watch": [
    "Specific warning sign 1 personalised to this person's condition.",
    "Specific warning sign 2."
  ],
  "injury_notes": "Specific management guidance for this person's reported injuries — not generic advice.",
  "nutrition_tip": "One highly specific nutrition recommendation directly tied to this person's problem and goal.",
  "red_flag_warnings": [],
  "recovery_advice": "Recovery guidance tailored to this person's training load, age, and condition."
}
""".strip()


# ── User Prompt Builder ──────────────────────────────────────────────────────

def _build_user_prompt(profile: dict, goal_mods: dict, sport_context: str,
                       injury_constraints: str) -> str:
    """
    Build the diagnosis-focused user prompt. The PRIMARY PROBLEM leads everything.
    """
    primary_problem = profile.get("primary_problem", "").strip()
    age            = profile.get("age", "unknown")
    gender         = profile.get("gender", "not specified")
    height         = profile.get("height_cm", "unknown")
    weight         = profile.get("weight_kg", "unknown")
    goal           = profile.get("main_goal", "General fitness")
    sport          = profile.get("sport", "").strip()
    fitness_level  = profile.get("fitness_level", "Beginner")
    training_days  = profile.get("training_days_per_week", 3)
    session_duration = profile.get("session_duration", "60 minutes")
    injuries       = profile.get("injuries", "None reported")
    pain_rating    = profile.get("pain_rating", 0)

    sport_line = f"Sport: {sport}" if sport else "Sport: Not applicable"

    prompt = f"""
=== PRIMARY PROBLEM (this is your main case to solve) ===
{primary_problem if primary_problem else "Not specified — use the profile below to infer the specific problem."}

=== CLIENT PROFILE ===
Age: {age} years
Gender: {gender}
Height: {height} cm | Weight: {weight} kg
Fitness level: {fitness_level}
Stated goal: {goal}
{sport_line}
Training days available: {training_days} days/week
Session duration: {session_duration}
Reported injuries/pain: {injuries if injuries else "None reported"}
Pain rating: {pain_rating}/10

=== TRAINING PARAMETERS ===
Rep range for this goal: {goal_mods.get("rep_range", "8-12")}
Rest periods: {goal_mods.get("rest_period", "60s")}
Intensity: {goal_mods.get("intensity", "moderate")}
Training focus: {goal_mods.get("focus", "general fitness")}
Avoid: {goal_mods.get("avoid", "nothing specific")}

=== SPORT CONTEXT ===
{sport_context}

=== INJURY AND MOVEMENT CONSTRAINTS ===
{injury_constraints}

=== YOUR TASK ===
1. Diagnose the specific root cause of this person's PRIMARY PROBLEM.
2. Design a {training_days}-session weekly plan that directly solves it.
3. Each session must be named after what it solves, not a generic label.
4. Every exercise must include a "why_you" that references this person's exact problem.
5. Give progress markers and warning signs specific to this case.
6. Sessions must fit within {session_duration}.
7. Match all exercise complexity to {fitness_level} level.
8. Return ONLY the JSON object — no markdown, no explanation outside JSON.
""".strip()

    return prompt


# ── Main Plan Generation Function ────────────────────────────────────────────

def generate_plan(profile: dict) -> dict:
    """
    Diagnose the user's specific problem and generate a targeted weekly plan.

    Args:
        profile: User fitness data including primary_problem from onboarding.

    Returns:
        A structured plan dict with diagnosis, solution, exercises, and markers.

    Raises:
        ValueError:   If the AI returns malformed JSON.
        RuntimeError: If the OpenAI API call fails.
    """
    goal         = profile.get("main_goal", "General fitness")
    sport        = profile.get("sport", "")
    injuries     = profile.get("injuries", "")
    pain_rating  = profile.get("pain_rating", 0)

    goal_mods          = get_goal_modifiers(goal)
    sport_context      = get_sport_context(sport)
    red_flag_warnings  = check_red_flags(injuries, pain_rating)
    injury_constraints = build_injury_constraints(injuries, pain_rating)

    user_prompt = _build_user_prompt(profile, goal_mods, sport_context, injury_constraints)

    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user",   "content": user_prompt},
            ],
            response_format={"type": "json_object"},
            temperature=0.5,   # Lower temperature = more precise, less hallucination
            max_tokens=4000,   # More tokens to allow detailed why_you explanations
        )
    except openai.OpenAIError as e:
        raise RuntimeError(f"OpenAI API error: {e}") from e

    raw_content = response.choices[0].message.content

    try:
        plan = json.loads(raw_content)
    except json.JSONDecodeError as e:
        raise ValueError(
            f"AI returned invalid JSON: {e}\n\nRaw response:\n{raw_content}"
        ) from e

    # Merge pre-computed red flag warnings with any the AI found.
    existing = plan.get("red_flag_warnings", [])
    plan["red_flag_warnings"] = list(dict.fromkeys(red_flag_warnings + existing))

    return plan
