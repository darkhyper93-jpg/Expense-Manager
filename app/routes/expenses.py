"""Expense CRUD, filtering, search, and CSV export."""

import csv
import io
from datetime import datetime

from flask import (
    Blueprint,
    Response,
    flash,
    redirect,
    render_template,
    request,
    url_for,
)
from flask_babel import gettext as _

from supabase_client import get_supabase
from utils import (
    get_current_user_id,
    login_required,
    validate_amount,
    validate_required_text,
)

expenses_bp = Blueprint('expenses', __name__, url_prefix='/expenses')


def _get_categories(user_id: str) -> list:
    supabase = get_supabase()
    result = (
        supabase.table('categories')
        .select('name, color, icon')
        .eq('user_id', user_id)
        .order('name')
        .execute()
    )
    return result.data or []


def _get_expense(user_id: str, expense_id: str):
    supabase = get_supabase()
    result = (
        supabase.table('expenses')
        .select('*')
        .eq('id', expense_id)
        .eq('user_id', user_id)
        .execute()
    )
    return result.data[0] if result.data else None


@expenses_bp.route('/')
@login_required
def list_expenses():
    """List expenses with optional filters."""
    user_id = get_current_user_id()
    supabase = get_supabase()

    query = (
        supabase.table('expenses')
        .select('*')
        .eq('user_id', user_id)
        .order('date', desc=True)
    )

    category = request.args.get('category', '').strip()
    date_from = request.args.get('date_from', '').strip()
    date_to = request.args.get('date_to', '').strip()
    search = request.args.get('search', '').strip()

    if category:
        query = query.eq('category', category)
    if date_from:
        query = query.gte('date', date_from)
    if date_to:
        query = query.lte('date', date_to)

    result = query.execute()
    expenses = result.data or []

    if search:
        search_lower = search.lower()
        expenses = [
            e for e in expenses
            if search_lower in (e.get('description') or '').lower()
        ]

    categories = _get_categories(user_id)
    return render_template(
        'expenses.html',
        expenses=expenses,
        categories=categories,
        filters={
            'category': category,
            'date_from': date_from,
            'date_to': date_to,
            'search': search,
        },
    )


@expenses_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add_expense():
    """Create a new expense."""
    user_id = get_current_user_id()
    categories = _get_categories(user_id)

    if request.method == 'POST':
        amount, err = validate_amount(request.form.get('amount', ''))
        category, err2 = validate_required_text(
            request.form.get('category', ''), 'category'
        )
        description = (request.form.get('description') or '').strip()
        exp_date = (request.form.get('date') or '').strip()

        if err:
            flash(err, 'error')
        elif err2:
            flash(err2, 'error')
        elif not exp_date:
            flash(_('Date is required.'), 'error')
        else:
            try:
                datetime.strptime(exp_date, '%Y-%m-%d')
                supabase = get_supabase()
                supabase.table('expenses').insert({
                    'user_id': user_id,
                    'amount': amount,
                    'category': category,
                    'description': description or None,
                    'date': exp_date,
                }).execute()
                flash(_('Expense added.'), 'success')
                return redirect(url_for('expenses.list_expenses'))
            except ValueError:
                flash(_('Invalid date format.'), 'error')
            except Exception as exc:
                flash(_('Failed to add expense: %(error)s') % {'error': str(exc)}, 'error')

    return render_template(
        'expenses.html',
        mode='add',
        categories=categories,
        expense=None,
        expenses=[],
        filters={},
    )


@expenses_bp.route('/<expense_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_expense(expense_id):
    """Update an existing expense."""
    user_id = get_current_user_id()
    expense = _get_expense(user_id, expense_id)
    if not expense:
        flash(_('Expense not found.'), 'error')
        return redirect(url_for('expenses.list_expenses'))

    categories = _get_categories(user_id)

    if request.method == 'POST':
        amount, err = validate_amount(request.form.get('amount', ''))
        category, err2 = validate_required_text(
            request.form.get('category', ''), 'category'
        )
        description = (request.form.get('description') or '').strip()
        exp_date = (request.form.get('date') or '').strip()

        if err:
            flash(err, 'error')
        elif err2:
            flash(err2, 'error')
        elif not exp_date:
            flash(_('Date is required.'), 'error')
        else:
            try:
                datetime.strptime(exp_date, '%Y-%m-%d')
                supabase = get_supabase()
                supabase.table('expenses').update({
                    'amount': amount,
                    'category': category,
                    'description': description or None,
                    'date': exp_date,
                }).eq('id', expense_id).eq('user_id', user_id).execute()
                flash(_('Expense updated.'), 'success')
                return redirect(url_for('expenses.list_expenses'))
            except ValueError:
                flash(_('Invalid date format.'), 'error')
            except Exception as exc:
                flash(_('Failed to update expense: %(error)s') % {'error': str(exc)}, 'error')

    return render_template(
        'expenses.html',
        mode='edit',
        categories=categories,
        expense=expense,
        expenses=[],
        filters={},
    )


@expenses_bp.route('/<expense_id>/delete', methods=['POST'])
@login_required
def delete_expense(expense_id):
    """Delete an expense after confirmation."""
    user_id = get_current_user_id()
    try:
        supabase = get_supabase()
        supabase.table('expenses').delete().eq(
            'id', expense_id
        ).eq('user_id', user_id).execute()
        flash(_('Expense deleted.'), 'success')
    except Exception as exc:
        flash(_('Failed to delete expense: %(error)s') % {'error': str(exc)}, 'error')

    return redirect(url_for('expenses.list_expenses'))


@expenses_bp.route('/export')
@login_required
def export_csv():
    """Export filtered expenses as CSV."""
    user_id = get_current_user_id()
    supabase = get_supabase()

    query = (
        supabase.table('expenses')
        .select('*')
        .eq('user_id', user_id)
        .order('date', desc=True)
    )

    date_from = request.args.get('date_from', '').strip()
    date_to = request.args.get('date_to', '').strip()
    if date_from:
        query = query.gte('date', date_from)
    if date_to:
        query = query.lte('date', date_to)

    result = query.execute()
    expenses = result.data or []

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow([
        _('Date'), _('Category'), _('Description'), _('Amount'),
    ])
    for exp in expenses:
        writer.writerow([
            exp['date'],
            exp['category'],
            exp.get('description') or '',
            exp['amount'],
        ])

    return Response(
        output.getvalue(),
        mimetype='text/csv',
        headers={
            'Content-Disposition': 'attachment; filename=expenses.csv',
        },
    )
