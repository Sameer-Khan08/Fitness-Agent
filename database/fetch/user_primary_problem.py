from database import get_db_connection

def get_user_medical_flags(user_id: int) -> list[str]:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT flag FROM user_medical_flags WHERE user_id = ?", (user_id,))
    rows = cursor.fetchall()
    conn.close()
    return [row['flag'] for row in rows]

def get_user_injuries(user_id: int) -> list[str]:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT injury FROM user_injuries WHERE user_id = ?", (user_id,))
    rows = cursor.fetchall()
    conn.close()
    return [row['injury'] for row in rows]
