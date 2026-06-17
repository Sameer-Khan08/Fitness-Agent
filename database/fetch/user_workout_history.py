from database import get_db

def get_user_workout_history(user_id: int) -> list[dict]:
    db = get_db()
    return db.fetchall("SELECT * FROM workout_history WHERE user_id = %s ORDER BY date DESC", (user_id,))

def add_workout_history(user_id: int, date: str, duration_minutes: int, calories_burned: int, notes: str):
    db = get_db()
    db.execute("""
        INSERT INTO workout_history (user_id, date, duration_minutes, calories_burned, notes)
        VALUES (%s, %s, %s, %s, %s)
    """, (user_id, date, duration_minutes, calories_burned, notes))
