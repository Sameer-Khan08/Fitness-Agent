from .database_postgres import get_db

# Remove Supabase client export
def get_supabase_client():
    raise NotImplementedError("Use get_db() instead")