from database import get_supabase_client

def get_user_by_username(username: str) -> dict | None:
    supabase = get_supabase_client()
    response = supabase.table("users").select("*").eq("username", username).execute()
    return response.data[0] if response.data else None

def get_user_profile(user_id: int) -> dict | None:
    supabase = get_supabase_client()
    response = supabase.table("user_profiles").select("*").eq("user_id", user_id).execute()
    return response.data[0] if response.data else None
