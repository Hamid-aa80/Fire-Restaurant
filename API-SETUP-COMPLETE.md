# Salt & Smoke Django API (Fire_Restaurant Project)

The backend is implemented with Django. Local development uses SQLite by
default; production requires persistent PostgreSQL configured with
`DATABASE_URL`. Django models define customers, tables, reservations,
newsletter signups, and menu items; Django forms validate API input; views
implement JSON API handlers; URL configuration maps the API; and Django admin
provides staff authentication and data management.

## Run locally

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate --fake-initial
python manage.py runserver 0.0.0.0:5000
```

The initial migration can reuse compatible legacy tables in `database.db`;
for a fresh database, migrations create the schema and seed the restaurant's
tables. Use `python manage.py createsuperuser` to create an administrator for
`/admin/` and staff-only API routes. Production migrations run as the Heroku
release phase.

See [API-QUICKSTART.md](API-QUICKSTART.md) for request examples,
[API-DOCUMENTATION.md](API-DOCUMENTATION.md) for the complete route reference,
and run `python manage.py test restaurant` for backend tests.
