"""Internationalization helpers and locale configuration."""

from flask import request, session
from flask_babel import Babel, gettext

# Supported locales: code -> display label
LANGUAGES = {
    'en': 'English',
    'es': 'Español',
    'pt_BR': 'Português',
    'fr': 'Français',
    'de': 'Deutsch',
    'it': 'Italiano',
}

# Flag emoji for the language selector
LANGUAGE_FLAGS = {
    'en': '🇺🇸',
    'es': '🇪🇸',
    'pt_BR': '🇧🇷',
    'fr': '🇫🇷',
    'de': '🇩🇪',
    'it': '🇮🇹',
}

# Canonical default category names stored in the database
DEFAULT_CATEGORY_NAMES = (
    'Food', 'Transport', 'Entertainment', 'Health', 'Education', 'Other'
)


def normalize_locale(code: str) -> str | None:
    """Map browser / user locale codes to a supported app locale."""
    if not code:
        return None
    normalized = code.replace('-', '_')
    if normalized in LANGUAGES:
        return normalized
    base = normalized.split('_')[0]
    if base in LANGUAGES:
        return base
    if base == 'pt':
        return 'pt_BR'
    return None


def get_locale():
    """Return the active locale for the current request."""
    if 'lang' in session:
        locale = normalize_locale(session['lang'])
        if locale:
            return locale

    best = request.accept_languages.best_match(LANGUAGES.keys())
    if best:
        return best

    for lang, _ in request.accept_languages:
        locale = normalize_locale(lang)
        if locale:
            return locale

    return 'en'


def translate_category(name: str) -> str:
    """Translate a known default category name for display."""
    labels = {
        'Food': gettext('Food'),
        'Transport': gettext('Transport'),
        'Entertainment': gettext('Entertainment'),
        'Health': gettext('Health'),
        'Education': gettext('Education'),
        'Other': gettext('Other'),
    }
    return labels.get(name, name)


def translate_budget_scope(name: str) -> str:
    """Translate budget scope labels (Global or category name)."""
    if name == 'Global':
        return gettext('Global')
    return translate_category(name)


def init_babel(app):
    """Initialize Flask-Babel on the application."""
    app.config.setdefault('BABEL_DEFAULT_LOCALE', 'en')
    app.config.setdefault('LANGUAGES', LANGUAGES)
    app.config.setdefault('BABEL_TRANSLATION_DIRECTORIES', 'translations')

    babel = Babel(app, locale_selector=get_locale)

    @app.context_processor
    def inject_i18n():
        from flask_babel import get_locale as babel_get_locale
        current = str(babel_get_locale())
        return {
            'LANGUAGES': LANGUAGES,
            'LANGUAGE_FLAGS': LANGUAGE_FLAGS,
            'current_locale': current,
            'translate_category': translate_category,
            'translate_budget_scope': translate_budget_scope,
        }

    return babel
