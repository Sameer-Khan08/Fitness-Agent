from database import get_db_connection

def get_user_goals(user_id: int) -> list[str]:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT goal FROM user_goals WHERE user_id = ?", (user_id,))
    rows = cursor.fetchall()
    conn.close()
    return [row['goal'] for row in rows]
