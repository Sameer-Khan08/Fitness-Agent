"""
utils.py
--------
Generic utility functions for TrainWise AI.
"""

import os

def get_deployment_checklist(root_dir: str, text_ai_enabled: bool, image_ai_enabled: bool, supabase_configured: bool) -> dict:
    """Check existence of essential files and configurations."""
    return {
        "requirements_txt": os.path.exists(os.path.join(root_dir, "requirements.txt")),
        "env_example": os.path.exists(os.path.join(root_dir, ".env.example")),
        "readme": os.path.exists(os.path.join(root_dir, "README.md")),
        "text_ai": text_ai_enabled,
        "images": image_ai_enabled,
        "supabase": supabase_configured,
    }
