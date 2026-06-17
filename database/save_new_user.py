from database import get_supabase_client

def create_user(username: str) -> int:
    """Create a new user and return their ID. Returns existing ID if user exists."""
    supabase = get_supabase_client()
    
    # Try to fetch first
    response = supabase.table("users").select("id").eq("username", username).execute()
    if response.data:
        return response.data[0]['id']
        
    # Insert new user
    response = supabase.table("users").insert({"username": username}).execute()
    return response.data[0]['id']

def save_user_profile_data(user_id: int, profile_data: dict):
    """Save the full profile dictionary to the database for the given user_id."""
    supabase = get_supabase_client()
    
    # 1. Save or update user_profiles
    supabase.table("user_profiles").upsert({
        "user_id": user_id,
        "age": profile_data.get('age'),
        "gender": profile_data.get('gender'),
        "fitness_level": profile_data.get('fitness_level'),
        "experience_years": profile_data.get('experience_years'),
        "medical_clearance": profile_data.get('medical_clearance'),
        "red_flags_present": profile_data.get('red_flags_present'),
        "training_status": profile_data.get('training_status'),
        "main_sport": profile_data.get('main_sport')
    }).execute()
    
    # 2. Save goals
    supabase.table("user_goals").delete().eq("user_id", user_id).execute()
    goal = profile_data.get('goal')
    if goal:
        supabase.table("user_goals").insert({"user_id": user_id, "goal": goal}).execute()
        
    # 3. Save medical flags
    supabase.table("user_medical_flags").delete().eq("user_id", user_id).execute()
    medical_flags = profile_data.get('medical_flags', [])
    if medical_flags:
        supabase.table("user_medical_flags").insert([
            {"user_id": user_id, "flag": flag} for flag in medical_flags
        ]).execute()
        
    # 4. Save injuries
    supabase.table("user_injuries").delete().eq("user_id", user_id).execute()
    injuries = profile_data.get('injuries', [])
    if injuries:
        supabase.table("user_injuries").insert([
            {"user_id": user_id, "injury": injury} for injury in injuries
        ]).execute()
