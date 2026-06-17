from database import get_db

def get_user_by_username(username: str) -> dict | None:
    db = get_db()
    return db.fetchone("SELECT * FROM users WHERE username = %s", (username,))

def get_user_profile(user_id: int) -> dict | None:
    db = get_db()
    return db.fetchone("SELECT * FROM user_profiles WHERE user_id = %s", (user_id,))
