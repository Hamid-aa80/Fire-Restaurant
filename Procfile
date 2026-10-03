release: python manage.py migrate --noinput
web: gunicorn salt_smoke.wsgi --bind 0.0.0.0:$PORT