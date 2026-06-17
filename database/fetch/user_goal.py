from database import get_supabase_client

def get_user_goals(user_id: int) -> list[str]:
    supabase = get_supabase_client()
    response = supabase.table("user_goals").select("goal").eq("user_id", user_id).execute()
    return [row['goal'] for row in response.data]
