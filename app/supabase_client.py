"""Supabase client factory with error handling helpers."""

from functools import wraps

from flask import flash
from supabase import Client, create_client

from config import Config


def get_supabase(use_service_role: bool = True) -> Client:
    """Return a Supabase client using service role or anon key."""
    key = (
        Config.SUPABASE_SERVICE_ROLE_KEY
        if use_service_role
        else Config.SUPABASE_ANON_KEY
    )
    return create_client(Config.SUPABASE_URL, key)


def handle_supabase_error(default_message: str = 'Database error occurred.'):
    """Decorator to catch Supabase errors and flash a user-friendly message."""

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as exc:
                flash(f'{default_message} ({exc})', 'error')
                return None

        return wrapper

    return decorator
