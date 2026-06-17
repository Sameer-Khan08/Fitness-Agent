from database import get_db

def create_user(username: str) -> int:
    """Create a new user and return their ID. Returns existing ID if user exists."""
    db = get_db()
    
    # Try to fetch first
    row = db.fetchone("SELECT id FROM users WHERE username = %s", (username,))
    if row:
        return row['id']
        
    # Insert new user returning ID
    return db.execute_returning_id("INSERT INTO users (username) VALUES (%s) RETURNING id", (username,))

def save_user_profile_data(user_id: int, profile_data: dict):
    """Save the full profile dictionary to the database for the given user_id."""
    db = get_db()
    
    # 1. Save or update user_profiles
    db.execute("""
        INSERT INTO user_profiles 
        (user_id, age, gender, fitness_level, experience_years, medical_clearance, red_flags_present, training_status, main_sport)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (user_id) DO UPDATE SET
            age = EXCLUDED.age,
            gender = EXCLUDED.gender,
            fitness_level = EXCLUDED.fitness_level,
            experience_years = EXCLUDED.experience_years,
            medical_clearance = EXCLUDED.medical_clearance,
            red_flags_present = EXCLUDED.red_flags_present,
            training_status = EXCLUDED.training_status,
            main_sport = EXCLUDED.main_sport
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
    db.execute("DELETE FROM user_goals WHERE user_id = %s", (user_id,))
    goal = profile_data.get('goal')
    if goal:
        db.execute("INSERT INTO user_goals (user_id, goal) VALUES (%s, %s)", (user_id, goal))
        
    # 3. Save medical flags
    db.execute("DELETE FROM user_medical_flags WHERE user_id = %s", (user_id,))
    for flag in profile_data.get('medical_flags', []):
        db.execute("INSERT INTO user_medical_flags (user_id, flag) VALUES (%s, %s)", (user_id, flag))
        
    # 4. Save injuries
    db.execute("DELETE FROM user_injuries WHERE user_id = %s", (user_id,))
    for injury in profile_data.get('injuries', []):
        db.execute("INSERT INTO user_injuries (user_id, injury) VALUES (%s, %s)", (user_id, injury))
