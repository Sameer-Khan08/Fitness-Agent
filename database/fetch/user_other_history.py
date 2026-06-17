from database import get_db

def get_daily_stats(user_id: int, limit: int = 7) -> list[dict]:
    db = get_db()
    return db.fetchall("SELECT * FROM daily_stats WHERE user_id = %s ORDER BY date DESC LIMIT %s", (user_id, limit))

def update_daily_stats(user_id: int, date: str, steps: int = 0, active_minutes: int = 0, calories_burned: int = 0):
    db = get_db()
    db.execute("""
        INSERT INTO daily_stats (user_id, date, steps, active_minutes, calories_burned)
        VALUES (%s, %s, %s, %s, %s)
        ON CONFLICT (user_id, date) DO UPDATE SET
            steps = daily_stats.steps + EXCLUDED.steps,
            active_minutes = daily_stats.active_minutes + EXCLUDED.active_minutes,
            calories_burned = daily_stats.calories_burned + EXCLUDED.calories_burned
    """, (user_id, date, steps, active_minutes, calories_burned))
