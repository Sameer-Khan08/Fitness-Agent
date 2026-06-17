from database import get_supabase_client

def get_user_medical_flags(user_id: int) -> list[str]:
    supabase = get_supabase_client()
    response = supabase.table("user_medical_flags").select("flag").eq("user_id", user_id).execute()
    return [row['flag'] for row in response.data]

def get_user_injuries(user_id: int) -> list[str]:
    supabase = get_supabase_client()
    response = supabase.table("user_injuries").select("injury").eq("user_id", user_id).execute()
    return [row['injury'] for row in response.data]
