from database import get_supabase_client

def get_user_workout_history(user_id: int) -> list[dict]:
    supabase = get_supabase_client()
    response = supabase.table("workout_history").select("*").eq("user_id", user_id).order("date", desc=True).execute()
    return response.data

def add_workout_history(user_id: int, date: str, duration_minutes: int, calories_burned: int, notes: str):
    supabase = get_supabase_client()
    supabase.table("workout_history").insert({
        "user_id": user_id,
        "date": date,
        "duration_minutes": duration_minutes,
        "calories_burned": calories_burned,
        "notes": notes
    }).execute()
