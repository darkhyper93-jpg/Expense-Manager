"""Legal pages: Privacy Policy and Terms of Service."""

from flask import Blueprint, render_template

legal_bp = Blueprint('legal', __name__)


@legal_bp.route('/privacy')
def privacy():
    """Display the privacy policy."""
    return render_template('privacy.html')


@legal_bp.route('/terms')
def terms():
    """Display the terms of service."""
    return render_template('terms.html')
