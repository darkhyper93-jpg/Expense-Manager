"""Authentication routes: register, login, logout."""

from flask import Blueprint, flash, redirect, render_template, request, session, url_for
from flask_babel import gettext as _

from supabase_client import get_supabase
from utils import create_default_categories, sync_user_record

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Authenticate user with Supabase Auth."""
    if session.get('user_id'):
        return redirect(url_for('dashboard.index'))

    if request.method == 'POST':
        email = (request.form.get('email') or '').strip().lower()
        password = request.form.get('password') or ''

        if not email or not password:
            flash(_('Email and password are required.'), 'error')
            return render_template('login.html')

        try:
            supabase = get_supabase(use_service_role=False)
            response = supabase.auth.sign_in_with_password({
                'email': email,
                'password': password,
            })
            user = response.user
            if not user:
                flash(_('Invalid credentials.'), 'error')
                return render_template('login.html')

            sync_user_record(user.id, user.email)
            session['user_id'] = user.id
            session['user_email'] = user.email
            session['access_token'] = response.session.access_token
            flash(_('Welcome back!'), 'success')
            return redirect(url_for('dashboard.index'))

        except Exception as exc:
            flash(_('Login failed: %(error)s') % {'error': str(exc)}, 'error')

    return render_template('login.html')


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """Register a new user via Supabase Auth."""
    if session.get('user_id'):
        return redirect(url_for('dashboard.index'))

    if request.method == 'POST':
        email = (request.form.get('email') or '').strip().lower()
        password = request.form.get('password') or ''
        confirm = request.form.get('confirm_password') or ''

        if not email or not password:
            flash(_('Email and password are required.'), 'error')
            return render_template('register.html')

        if len(password) < 6:
            flash(_('Password must be at least 6 characters.'), 'error')
            return render_template('register.html')

        if password != confirm:
            flash(_('Passwords do not match.'), 'error')
            return render_template('register.html')

        try:
            supabase = get_supabase(use_service_role=False)
            response = supabase.auth.sign_up({
                'email': email,
                'password': password,
            })
            user = response.user
            if not user:
                flash(_('Registration failed. Please try again.'), 'error')
                return render_template('register.html')

            sync_user_record(user.id, email)
            create_default_categories(user.id)

            session['user_id'] = user.id
            session['user_email'] = email
            if response.session:
                session['access_token'] = response.session.access_token

            flash(_('Account created successfully!'), 'success')
            return redirect(url_for('dashboard.index'))

        except Exception as exc:
            flash(_('Registration failed: %(error)s') % {'error': str(exc)}, 'error')

    return render_template('register.html')


@auth_bp.route('/logout')
def logout():
    """Clear session and log out, preserving language preference."""
    lang = session.get('lang')
    session.clear()
    if lang:
        session['lang'] = lang
    flash(_('You have been logged out.'), 'success')
    return redirect(url_for('auth.login'))
