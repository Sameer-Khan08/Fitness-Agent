import os
from supabase import create_client, Client
from src.config.settings import SUPABASE_URL, SUPABASE_KEY

# Cache the client instance
_supabase_client: Client | None = None

def get_supabase_client() -> Client:
    """Returns the initialized Supabase client."""
    global _supabase_client
    if not _supabase_client:
        if not SUPABASE_URL or not SUPABASE_KEY:
            raise ValueError("SUPABASE_URL and SUPABASE_KEY must be set in .env")
        _supabase_client = create_client(SUPABASE_URL, SUPABASE_KEY)
    return _supabase_client