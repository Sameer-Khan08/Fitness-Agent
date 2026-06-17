from database import get_db_connection

def get_user_workout_history(user_id: int) -> list[dict]:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM workout_history WHERE user_id = ? ORDER BY date DESC", (user_id,))
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def add_workout_history(user_id: int, date: str, duration_minutes: int, calories_burned: int, notes: str):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO workout_history (user_id, date, duration_minutes, calories_burned, notes) VALUES (?, ?, ?, ?, ?)",
        (user_id, date, duration_minutes, calories_burned, notes)
    )
    conn.commit()
    conn.close()
