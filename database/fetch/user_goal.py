from database import get_db

def get_user_goals(user_id: int) -> list[str]:
    db = get_db()
    rows = db.fetchall("SELECT goal FROM user_goals WHERE user_id = %s", (user_id,))
    return [row['goal'] for row in rows]
