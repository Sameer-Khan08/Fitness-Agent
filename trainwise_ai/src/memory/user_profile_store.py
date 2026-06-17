"""
user_profile_store.py
---------------------
Provides in-memory storage for the user's fitness profile.
No database is used at this stage — data lives only for the
duration of the Python process.
"""

# Internal variable that holds the user profile.
# Starts as None until a profile is saved.
_user_profile: dict | None = None


def save_profile(profile: dict) -> None:
    """
    Save a user profile to memory.

    Args:
        profile: A dictionary containing the user's fitness data.
    """
    global _user_profile
    _user_profile = profile


def get_profile() -> dict | None:
    """
    Retrieve the stored user profile.

    Returns:
        The profile dictionary, or None if no profile has been saved yet.
    """
    return _user_profile


def clear_profile() -> None:
    """
    Clear the stored user profile from memory.
    """
    global _user_profile
    _user_profile = None


def has_profile() -> bool:
    """
    Check whether a user profile is currently stored.

    Returns:
        True if a profile exists, False otherwise.
    """
    return _user_profile is not None
