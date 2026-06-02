"""Application configuration loaded from environment variables."""

import os
from pathlib import Path

from dotenv import load_dotenv

# Load .env from project root or app directory
load_dotenv()
load_dotenv(Path(__file__).parent.parent / '.env')


class Config:
    """Flask and Supabase configuration."""

    SECRET_KEY = os.environ.get('FLASK_SECRET_KEY', 'dev-secret-change-me')
    FLASK_ENV = os.environ.get('FLASK_ENV', 'development')
    DEBUG = FLASK_ENV == 'development'

    SUPABASE_URL = os.environ.get('SUPABASE_URL', '')
    SUPABASE_ANON_KEY = os.environ.get('SUPABASE_ANON_KEY', '')
    SUPABASE_SERVICE_ROLE_KEY = os.environ.get('SUPABASE_SERVICE_ROLE_KEY', '')

    WTF_CSRF_ENABLED = True
    WTF_CSRF_TIME_LIMIT = None

    # Default categories created for new users
    DEFAULT_CATEGORIES = [
        {'name': 'Food', 'color': '#ef4444', 'icon': '🍔'},
        {'name': 'Transport', 'color': '#3b82f6', 'icon': '🚗'},
        {'name': 'Entertainment', 'color': '#a855f7', 'icon': '🎬'},
        {'name': 'Health', 'color': '#22c55e', 'icon': '💊'},
        {'name': 'Education', 'color': '#f59e0b', 'icon': '📚'},
        {'name': 'Other', 'color': '#6b7280', 'icon': '📦'},
    ]
