"""Shared utilities: auth decorator, validation, default categories."""

from functools import wraps

from flask import redirect, session, url_for
from flask_babel import gettext as _

from config import Config
from supabase_client import get_supabase


def login_required(view):
    """Redirect unauthenticated users to the login page."""

    @wraps(view)
    def wrapped(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('auth.login'))
        return view(*args, **kwargs)

    return wrapped


def get_current_user_id() -> str | None:
    """Return the authenticated user's UUID from the session."""
    return session.get('user_id')


def create_default_categories(user_id: str) -> None:
    """Insert default expense categories for a new user."""
    supabase = get_supabase()
    rows = [
        {
            'user_id': user_id,
            'name': cat['name'],
            'color': cat['color'],
            'icon': cat['icon'],
        }
        for cat in Config.DEFAULT_CATEGORIES
    ]
    supabase.table('categories').insert(rows).execute()


def sync_user_record(user_id: str, email: str) -> None:
    """Ensure the public users table has a row for this auth user."""
    supabase = get_supabase()
    existing = (
        supabase.table('users')
        .select('id')
        .eq('id', user_id)
        .execute()
    )
    if not existing.data:
        supabase.table('users').insert({
            'id': user_id,
            'email': email,
        }).execute()


def validate_amount(value: str) -> tuple[float | None, str | None]:
    """Parse and validate a monetary amount."""
    try:
        amount = float(value)
        if amount <= 0:
            return None, _('Amount must be greater than zero.')
        return round(amount, 2), None
    except (TypeError, ValueError):
        return None, _('Invalid amount.')


def validate_required_text(value: str, field_key: str) -> tuple[str | None, str | None]:
    """Validate a required text field."""
    cleaned = (value or '').strip()
    if not cleaned:
        labels = {
            'category': _('Category'),
            'name': _('Name'),
        }
        label = labels.get(field_key, field_key)
        return None, _('%(field)s is required.') % {'field': label}
    return cleaned, None
