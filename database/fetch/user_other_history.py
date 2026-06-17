from database import get_db_connection

def get_daily_stats(user_id: int, limit: int = 7) -> list[dict]:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM daily_stats WHERE user_id = ? ORDER BY date DESC LIMIT ?", (user_id, limit))
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def update_daily_stats(user_id: int, date: str, steps: int = 0, active_minutes: int = 0, calories_burned: int = 0):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO daily_stats (user_id, date, steps, active_minutes, calories_burned)
        VALUES (?, ?, ?, ?, ?)
        ON CONFLICT(user_id, date) DO UPDATE SET
            steps = steps + excluded.steps,
            active_minutes = active_minutes + excluded.active_minutes,
            calories_burned = calories_burned + excluded.calories_burned
    """, (user_id, date, steps, active_minutes, calories_burned))
    conn.commit()
    conn.close()
