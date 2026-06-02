"""Language switching route."""

from flask import Blueprint, redirect, request, session, url_for

from i18n import LANGUAGES, normalize_locale

language_bp = Blueprint('language', __name__)


@language_bp.route('/set-language/<lang>')
def set_language(lang):
    """Persist language choice in session and redirect back."""
    locale = normalize_locale(lang)
    if locale and locale in LANGUAGES:
        session['lang'] = locale

    next_url = request.args.get('next') or request.referrer
    if not next_url or not next_url.startswith('/'):
        next_url = url_for('dashboard.index') if session.get('user_id') else url_for('auth.login')
    return redirect(next_url)
