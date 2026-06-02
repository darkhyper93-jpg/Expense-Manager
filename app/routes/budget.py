"""Budget tracking routes."""

from collections import defaultdict
from datetime import date

from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_babel import gettext as _

from supabase_client import get_supabase
from utils import get_current_user_id, login_required, validate_amount

budget_bp = Blueprint('budget', __name__, url_prefix='/budget')


def _fetch_budgets(user_id: str) -> list:
    supabase = get_supabase()
    result = (
        supabase.table('budgets')
        .select('*')
        .eq('user_id', user_id)
        .execute()
    )
    return result.data or []


def _month_spending(user_id: str) -> dict[str, float]:
    """Return spending by category for the current month."""
    today = date.today()
    month_start = today.replace(day=1).isoformat()
    supabase = get_supabase()
    result = (
        supabase.table('expenses')
        .select('category, amount')
        .eq('user_id', user_id)
        .gte('date', month_start)
        .execute()
    )
    totals: dict[str, float] = defaultdict(float)
    global_total = 0.0
    for exp in result.data or []:
        amount = float(exp['amount'])
        totals[exp['category']] += amount
        global_total += amount
    totals['__global__'] = global_total
    return totals


def _budget_status(spent: float, limit: float) -> str:
    if limit <= 0:
        return 'none'
    pct = spent / limit * 100
    if pct > 100:
        return 'exceeded'
    if pct > 80:
        return 'warning'
    return 'ok'


@budget_bp.route('/')
@login_required
def index():
    """Show budget settings and progress indicators."""
    user_id = get_current_user_id()
    budgets = _fetch_budgets(user_id)
    spending = _month_spending(user_id)

    supabase = get_supabase()
    categories = (
        supabase.table('categories')
        .select('name, color, icon')
        .eq('user_id', user_id)
        .order('name')
        .execute()
    ).data or []

    budget_items = []
    for b in budgets:
        cat = b.get('category')
        limit = float(b['amount'])
        spent = spending.get(cat or '__global__', 0.0)
        budget_items.append({
            'id': b['id'],
            'category': cat or 'Global',
            'limit': limit,
            'spent': round(spent, 2),
            'remaining': round(limit - spent, 2),
            'status': _budget_status(spent, limit),
            'pct': round(min(spent / limit * 100, 100), 1) if limit else 0,
        })

    return render_template(
        'budget.html',
        budget_items=budget_items,
        categories=categories,
    )


@budget_bp.route('/set', methods=['POST'])
@login_required
def set_budget():
    """Create or update a monthly budget."""
    user_id = get_current_user_id()
    amount, err = validate_amount(request.form.get('amount', ''))
    category = (request.form.get('category') or '').strip() or None

    if err:
        flash(err, 'error')
        return redirect(url_for('budget.index'))

    try:
        supabase = get_supabase()
        existing = (
            supabase.table('budgets')
            .select('id')
            .eq('user_id', user_id)
        )
        if category:
            existing = existing.eq('category', category)
        else:
            existing = existing.is_('category', 'null')

        row = existing.execute()
        if row.data:
            supabase.table('budgets').update({
                'amount': amount,
            }).eq('id', row.data[0]['id']).execute()
        else:
            supabase.table('budgets').insert({
                'user_id': user_id,
                'category': category,
                'amount': amount,
            }).execute()

        label = category or _('Global')
        flash(_('Budget for %(label)s saved.') % {'label': label}, 'success')
    except Exception as exc:
        flash(_('Failed to save budget: %(error)s') % {'error': str(exc)}, 'error')

    return redirect(url_for('budget.index'))


@budget_bp.route('/<budget_id>/delete', methods=['POST'])
@login_required
def delete_budget(budget_id):
    """Remove a budget entry."""
    user_id = get_current_user_id()
    try:
        supabase = get_supabase()
        supabase.table('budgets').delete().eq(
            'id', budget_id
        ).eq('user_id', user_id).execute()
        flash(_('Budget removed.'), 'success')
    except Exception as exc:
        flash(_('Failed to delete budget: %(error)s') % {'error': str(exc)}, 'error')

    return redirect(url_for('budget.index'))
