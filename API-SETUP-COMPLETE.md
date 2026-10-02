# Fire_Restaurant Django API

The backend is implemented with Django and SQLite. Django models define
reservations, newsletter signups, and menu items; Django forms validate API
input; views implement JSON API handlers; URL configuration maps the API; and
Django admin provides staff authentication and data management.

## Run locally

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate --fake-initial
python manage.py runserver 0.0.0.0:5000
```

The initial migration maps the Django models onto the existing `database.db`
tables. Use `python manage.py createsuperuser` to create an administrator for
`/admin/` and for staff-only API routes.

See [API-QUICKSTART.md](API-QUICKSTART.md) for request examples,
[API-DOCUMENTATION.md](API-DOCUMENTATION.md) for the complete route reference,
and run `python manage.py test restaurant` for backend tests.
