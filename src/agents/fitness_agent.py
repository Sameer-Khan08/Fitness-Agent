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
