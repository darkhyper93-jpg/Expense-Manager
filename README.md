# Expense Manager

Gestor de gastos personales para la web. Cada usuario registra sus gastos, los ordena por categoría, fija presupuestos mensuales y ve en un panel cuánto lleva gastado.

## Qué hace

- **Cuenta propia:** registro e inicio de sesión con correo y contraseña (Supabase Auth). Cada usuario ve solo sus datos.
- **Panel:** lo gastado este mes y este año, el presupuesto que queda, gastos por mes de los últimos seis meses, reparto por categoría del mes actual y los últimos movimientos.
- **Gastos:** alta, edición y borrado, con filtros por fechas y categoría y búsqueda por descripción.
- **Categorías:** propias, con nombre, color e ícono, además de las de serie.
- **Presupuestos:** mensual global o por categoría, con aviso al pasar el 80 % y al superar el 100 %.
- **Exportar** los gastos a CSV, filtrados por fechas.
- **Seis idiomas:** español, inglés, portugués de Brasil, francés, alemán e italiano (Flask-Babel). Se detecta el del navegador y se puede cambiar desde el menú.
- Interfaz oscura, adaptada a celular y escritorio, con protección CSRF en todos los formularios.

## Tecnología

Python con Flask (blueprints y plantillas Jinja2), Supabase (PostgreSQL y autenticación), Chart.js para los gráficos y Gunicorn para producción.

## Ponerlo en marcha

1. Crear un proyecto en [Supabase](https://supabase.com) y ejecutar `supabase/schema.sql` en su editor SQL.
2. Copiar `.env.example` como `.env` y completar las claves del proyecto y una `FLASK_SECRET_KEY` cualquiera.
3. Instalar y arrancar:

```bash
pip install -r requirements.txt
python run.py
```

La aplicación queda en http://localhost:5000.

**Producción:** el `Procfile` arranca la aplicación con Gunicorn, listo para Render o Railway. Las variables de entorno se cargan en el panel del servicio, nunca en el repositorio.

## Estructura

```
app/
  app.py              aplicación y registro de blueprints
  routes/             auth, dashboard, expenses, categories, budget, language, legal
  templates/          páginas Jinja2
  static/             estilos y scripts (gráficos)
  translations/       los cinco idiomas además del inglés
supabase/schema.sql   tablas e índices
docs/especificacion/  la especificación original: aplicación, interfaz e idiomas
```

---

**In English:** a personal expense tracker built with Flask and Supabase. Users log expenses, organize them into categories, set monthly budgets (global or per category) with 80 % and 100 % alerts, browse a dashboard with Chart.js charts and export to CSV. Available in six languages. Setup: run `supabase/schema.sql`, fill `.env` from `.env.example`, then `pip install -r requirements.txt` and `python run.py`.
