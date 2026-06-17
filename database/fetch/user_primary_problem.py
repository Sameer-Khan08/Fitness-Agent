from database import get_db

def get_user_medical_flags(user_id: int) -> list[str]:
    db = get_db()
    rows = db.fetchall("SELECT flag FROM user_medical_flags WHERE user_id = %s", (user_id,))
    return [row['flag'] for row in rows]

def get_user_injuries(user_id: int) -> list[str]:
    db = get_db()
    rows = db.fetchall("SELECT injury FROM user_injuries WHERE user_id = %s", (user_id,))
    return [row['injury'] for row in rows]
