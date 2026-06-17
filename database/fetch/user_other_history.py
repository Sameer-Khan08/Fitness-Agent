from database import get_supabase_client

def get_daily_stats(user_id: int, limit: int = 7) -> list[dict]:
    supabase = get_supabase_client()
    response = supabase.table("daily_stats").select("*").eq("user_id", user_id).order("date", desc=True).limit(limit).execute()
    return response.data

def update_daily_stats(user_id: int, date: str, steps: int = 0, active_minutes: int = 0, calories_burned: int = 0):
    supabase = get_supabase_client()
    
    # Try to fetch existing
    response = supabase.table("daily_stats").select("*").eq("user_id", user_id).eq("date", date).execute()
    if response.data:
        existing = response.data[0]
        supabase.table("daily_stats").update({
            "steps": existing.get("steps", 0) + steps,
            "active_minutes": existing.get("active_minutes", 0) + active_minutes,
            "calories_burned": existing.get("calories_burned", 0) + calories_burned
        }).eq("id", existing["id"]).execute()
    else:
        supabase.table("daily_stats").insert({
            "user_id": user_id,
            "date": date,
            "steps": steps,
            "active_minutes": active_minutes,
            "calories_burned": calories_burned
        }).execute()
