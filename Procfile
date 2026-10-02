release: python manage.py migrate
web: gunicorn salt_smoke.wsgi --bind 0.0.0.0:$PORT