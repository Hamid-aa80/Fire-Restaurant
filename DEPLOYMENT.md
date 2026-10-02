# Django Deployment

The backend is a Django application. Deploy it to a Python-capable host using
the WSGI entry point `salt_smoke.wsgi:application`.

## Production checklist

1. Use Python 3.10 or later and install dependencies with
   `pip install -r requirements.txt`.
2. Set `DJANGO_SECRET_KEY` to a long, private value.
3. Set `DJANGO_DEBUG=false` and `DJANGO_ALLOWED_HOSTS` to the deployed host
   names, comma-separated.
4. Configure `DATABASE_NAME` to a persistent SQLite file path, or configure a
   production database backend before deploying at scale.
5. Run `python manage.py migrate` for a fresh database. To adopt the existing
   SQLite tables, run `python manage.py migrate --fake-initial` instead.
6. Run `python manage.py createsuperuser` to provision a staff administrator.
7. Collect Django static assets with `python manage.py collectstatic` and serve
   them through the host or a web server.
8. Use the platform's WSGI process manager to serve `salt_smoke.wsgi:application`;
   do not use Django's development server in production.

The existing GitHub Pages URL hosts only the static frontend and cannot run
this Django backend. Deploy the backend separately and configure the frontend
to call the backend's public URL if those origins differ.
