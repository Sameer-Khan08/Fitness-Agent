from database import get_db_connection

def create_user(username: str) -> int:
    """Create a new user and return their ID. Returns existing ID if user exists."""
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        # Try to insert
        cursor.execute("INSERT INTO users (username) VALUES (?)", (username,))
        user_id = cursor.lastrowid
        conn.commit()
    except Exception:
        # If exists, fetch ID
        cursor.execute("SELECT id FROM users WHERE username = ?", (username,))
        row = cursor.fetchone()
        user_id = row['id'] if row else None
    finally:
        conn.close()
    return user_id

def save_user_profile_data(user_id: int, profile_data: dict):
    """Save the full profile dictionary to the database for the given user_id."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # 1. Save or update user_profiles
    cursor.execute("""
        INSERT INTO user_profiles 
        (user_id, age, gender, fitness_level, experience_years, medical_clearance, red_flags_present, training_status, main_sport)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(user_id) DO UPDATE SET
            age=excluded.age,
            gender=excluded.gender,
            fitness_level=excluded.fitness_level,
            experience_years=excluded.experience_years,
            medical_clearance=excluded.medical_clearance,
            red_flags_present=excluded.red_flags_present,
            training_status=excluded.training_status,
            main_sport=excluded.main_sport
    """, (
        user_id,
        profile_data.get('age'),
        profile_data.get('gender'),
        profile_data.get('fitness_level'),
        profile_data.get('experience_years'),
        profile_data.get('medical_clearance'),
        profile_data.get('red_flags_present'),
        profile_data.get('training_status'),
        profile_data.get('main_sport')
    ))
    
    # 2. Save goals
    cursor.execute("DELETE FROM user_goals WHERE user_id = ?", (user_id,))
    goal = profile_data.get('goal')
    if goal:
        cursor.execute("INSERT INTO user_goals (user_id, goal) VALUES (?, ?)", (user_id, goal))
        
    # 3. Save medical flags
    cursor.execute("DELETE FROM user_medical_flags WHERE user_id = ?", (user_id,))
    for flag in profile_data.get('medical_flags', []):
        cursor.execute("INSERT INTO user_medical_flags (user_id, flag) VALUES (?, ?)", (user_id, flag))
        
    # 4. Save injuries
    cursor.execute("DELETE FROM user_injuries WHERE user_id = ?", (user_id,))
    for injury in profile_data.get('injuries', []):
        cursor.execute("INSERT INTO user_injuries (user_id, injury) VALUES (?, ?)", (user_id, injury))
        
    conn.commit()
    conn.close()
