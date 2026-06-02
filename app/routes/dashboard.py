"""Dashboard routes with summary stats and chart data."""

from collections import defaultdict
from datetime import date, datetime

from flask import Blueprint, render_template
from flask_babel import format_date

from i18n import translate_category
from supabase_client import get_supabase
from utils import get_current_user_id, login_required

dashboard_bp = Blueprint('dashboard', __name__)


def _month_key(d: date) -> str:
    return d.strftime('%Y-%m')


def _fetch_user_expenses(user_id: str):
    supabase = get_supabase()
    result = (
        supabase.table('expenses')
        .select('*')
        .eq('user_id', user_id)
        .order('date', desc=True)
        .execute()
    )
    return result.data or []


def _fetch_budgets(user_id: str):
    supabase = get_supabase()
    result = (
        supabase.table('budgets')
        .select('*')
        .eq('user_id', user_id)
        .execute()
    )
    return result.data or []


@dashboard_bp.route('/')
@login_required
def index():
    """Main dashboard with totals, charts, and recent transactions."""
    user_id = get_current_user_id()
    today = date.today()
    month_start = today.replace(day=1)
    year_start = today.replace(month=1, day=1)

    expenses = _fetch_user_expenses(user_id)
    budgets = _fetch_budgets(user_id)

    month_total = 0.0
    year_total = 0.0
    category_totals: dict[str, float] = defaultdict(float)
    monthly_totals: dict[str, float] = defaultdict(float)

    # Build last 6 month labels
    month_labels = []
    for i in range(5, -1, -1):
        m = today.month - i
        y = today.year
        while m <= 0:
            m += 12
            y -= 1
        month_labels.append(f'{y}-{m:02d}')

    for exp in expenses:
        exp_date = datetime.fromisoformat(exp['date']).date() if isinstance(
            exp['date'], str
        ) else exp['date']
        amount = float(exp['amount'])
        key = _month_key(exp_date)
        monthly_totals[key] += amount

        if exp_date >= month_start:
            month_total += amount
            category_totals[exp['category']] += amount

        if exp_date >= year_start:
            year_total += amount

    bar_labels = []
    bar_values = []
    for label in month_labels:
        y, m = label.split('-')
        dt = date(int(y), int(m), 1)
        bar_labels.append(format_date(dt, format='MMM yyyy'))
        bar_values.append(round(monthly_totals.get(label, 0), 2))

    pie_keys = list(category_totals.keys())
    pie_labels = [translate_category(c) for c in pie_keys]
    pie_values = [round(category_totals[c], 2) for c in pie_keys]

    global_budget = next(
        (b for b in budgets if b.get('category') is None), None
    )
    remaining_budget = None
    budget_status = 'none'
    if global_budget:
        limit = float(global_budget['amount'])
        remaining_budget = round(limit - month_total, 2)
        pct = (month_total / limit * 100) if limit > 0 else 0
        if pct > 100:
            budget_status = 'exceeded'
        elif pct > 80:
            budget_status = 'warning'
        else:
            budget_status = 'ok'

    recent = expenses[:5]

    return render_template(
        'dashboard.html',
        month_total=round(month_total, 2),
        year_total=round(year_total, 2),
        remaining_budget=remaining_budget,
        budget_status=budget_status,
        bar_labels=bar_labels,
        bar_values=bar_values,
        pie_labels=pie_labels,
        pie_values=pie_values,
        recent_expenses=recent,
    )
