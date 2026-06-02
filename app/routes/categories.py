"""Category management routes."""

from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_babel import gettext as _

from supabase_client import get_supabase
from utils import get_current_user_id, login_required, validate_required_text

categories_bp = Blueprint('categories', __name__, url_prefix='/categories')


def _get_categories(user_id: str) -> list:
    supabase = get_supabase()
    result = (
        supabase.table('categories')
        .select('*')
        .eq('user_id', user_id)
        .order('name')
        .execute()
    )
    return result.data or []


@categories_bp.route('/')
@login_required
def list_categories():
    """Display all categories for the current user."""
    user_id = get_current_user_id()
    categories = _get_categories(user_id)
    return render_template('categories.html', categories=categories)


@categories_bp.route('/add', methods=['POST'])
@login_required
def add_category():
    """Create a custom category."""
    user_id = get_current_user_id()
    name, err = validate_required_text(request.form.get('name', ''), 'name')
    color = (request.form.get('color') or '#6366f1').strip()
    icon = (request.form.get('icon') or '📁').strip()

    if err:
        flash(err, 'error')
        return redirect(url_for('categories.list_categories'))

    try:
        supabase = get_supabase()
        supabase.table('categories').insert({
            'user_id': user_id,
            'name': name,
            'color': color,
            'icon': icon,
        }).execute()
        flash(_('Category created.'), 'success')
    except Exception as exc:
        flash(_('Failed to create category: %(error)s') % {'error': str(exc)}, 'error')

    return redirect(url_for('categories.list_categories'))


@categories_bp.route('/<category_id>/delete', methods=['POST'])
@login_required
def delete_category(category_id):
    """Delete category and reassign its expenses to Other."""
    user_id = get_current_user_id()
    supabase = get_supabase()

    try:
        cat_result = (
            supabase.table('categories')
            .select('name')
            .eq('id', category_id)
            .eq('user_id', user_id)
            .execute()
        )
        if not cat_result.data:
            flash(_('Category not found.'), 'error')
            return redirect(url_for('categories.list_categories'))

        cat_name = cat_result.data[0]['name']
        if cat_name == 'Other':
            flash(_('Cannot delete the Other category.'), 'error')
            return redirect(url_for('categories.list_categories'))

        other = (
            supabase.table('categories')
            .select('id')
            .eq('user_id', user_id)
            .eq('name', 'Other')
            .execute()
        )
        if not other.data:
            supabase.table('categories').insert({
                'user_id': user_id,
                'name': 'Other',
                'color': '#6b7280',
                'icon': '📦',
            }).execute()

        supabase.table('expenses').update({
            'category': 'Other',
        }).eq('user_id', user_id).eq('category', cat_name).execute()

        supabase.table('budgets').delete().eq(
            'user_id', user_id
        ).eq('category', cat_name).execute()

        supabase.table('categories').delete().eq(
            'id', category_id
        ).eq('user_id', user_id).execute()

        flash(
            _('Category "%(name)s" deleted. Expenses moved to Other.')
            % {'name': cat_name},
            'success',
        )
    except Exception as exc:
        flash(_('Failed to delete category: %(error)s') % {'error': str(exc)}, 'error')

    return redirect(url_for('categories.list_categories'))
