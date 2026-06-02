Build a full-stack personal expense manager web app with the following specifications:

## STACK
- Backend: Python + Flask
- Database: Supabase (PostgreSQL)
- Frontend: HTML + CSS + JavaScript (Jinja2 templates)
- Charts: Chart.js
- Hosting: Cloudflare Pages (frontend) + Railway or Render (backend)
- Auth: Supabase Auth (email/password)

## DATABASE SCHEMA (Supabase)

Table: users
- id (uuid, primary key, auto)
- email (text, unique)
- created_at (timestamp)

Table: expenses
- id (uuid, primary key, auto)
- user_id (uuid, foreign key → users.id)
- amount (float, not null)
- category (text, not null)
- description (text)
- date (date, not null)
- created_at (timestamp)

Table: categories
- id (uuid, primary key, auto)
- user_id (uuid, foreign key → users.id)
- name (text, not null)
- color (text) → hex color for charts
- icon (text) → emoji or icon name

## FEATURES

1. Auth
   - Register with email/password
   - Login/logout
   - Protected routes (redirect to login if not authenticated)
   - Session handling with Flask session

2. Dashboard (home after login)
   - Total spent this month
   - Total spent this year
   - Remaining budget (if budget is set)
   - Bar chart: expenses by month (last 6 months)
   - Pie chart: expenses by category (current month)
   - Last 5 transactions listed

3. Expenses
   - Add expense: amount, category, description, date
   - Edit expense
   - Delete expense
   - List all expenses with filters: by date range, by category
   - Search by description

4. Categories
   - Create custom categories with name and color
   - Default categories: Food, Transport, Entertainment, Health, Education, Other
   - Delete category (reassign expenses to "Other")

5. Budget
   - Set monthly budget per category or global
   - Visual indicator when approaching or exceeding budget (yellow > 80%, red > 100%)

6. Export
   - Export expenses to CSV filtered by date range

## FLASK PROJECT STRUCTURE
/app
/static
/css → styles.css
/js → charts.js, main.js
/templates
base.html
login.html
register.html
dashboard.html
expenses.html
categories.html
budget.html
/routes
auth.py
expenses.py
categories.py
budget.py
dashboard.py
config.py
app.py
supabase_client.py

## SECURITY REQUIREMENTS
- All routes protected with login_required decorator
- User can only access their own data (filter all queries by user_id)
- Input validation on all forms (server-side)
- Environment variables for Supabase keys (never hardcoded)
- CSRF protection on all forms
- Passwords handled entirely by Supabase Auth (never stored manually)

## UI/UX REQUIREMENTS
- Responsive design (mobile + desktop)
- Clean, minimal dark or light theme (user toggle)
- Loading states on async operations
- Success/error toast notifications
- Empty states with helpful messages when no data exists
- Confirm dialog before deleting anything

## ENVIRONMENT VARIABLES NEEDED
SUPABASE_URL=
SUPABASE_ANON_KEY=
SUPABASE_SERVICE_ROLE_KEY=
FLASK_SECRET_KEY=
FLASK_ENV=development

## IMPLEMENTATION ORDER
1. Set up Flask app and Supabase connection
2. Implement auth (register, login, logout, session)
3. Create database tables in Supabase
4. Implement expense CRUD
5. Implement categories
6. Build dashboard with Chart.js
7. Implement budget tracking
8. Add CSV export
9. Polish UI and add responsiveness
10. Deploy to Render + Cloudflare

Generate clean, well-commented code. Use Flask blueprints for route organization. 
Handle all Supabase errors gracefully. Follow Python PEP8 style conventions.