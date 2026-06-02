"""Flask application factory."""

from datetime import datetime

from flask import Flask, session
from flask_wtf.csrf import CSRFProtect

from config import Config
from i18n import init_babel
from routes.auth import auth_bp
from routes.budget import budget_bp
from routes.categories import categories_bp
from routes.dashboard import dashboard_bp
from routes.expenses import expenses_bp
from routes.language import language_bp
from routes.legal import legal_bp


def create_app() -> Flask:
    """Create and configure the Flask application."""
    app = Flask(__name__)
    app.config.from_object(Config)

    CSRFProtect(app)
    init_babel(app)

    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(expenses_bp)
    app.register_blueprint(categories_bp)
    app.register_blueprint(budget_bp)
    app.register_blueprint(language_bp)
    app.register_blueprint(legal_bp)

    @app.context_processor
    def inject_globals():
        return {
            'current_user_email': session.get('user_email', ''),
            'current_year': datetime.now().year,
        }

    return app


app = create_app()
