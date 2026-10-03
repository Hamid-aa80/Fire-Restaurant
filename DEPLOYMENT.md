# Deploy Fire_Restaurant to Heroku

The README's [Heroku Deployment](README.md#heroku-deployment) section is the
complete, current deployment procedure, including repository preparation,
dependency installation, environment configuration, Postgres migrations,
deployment, and final verification. This guide provides the corresponding
Heroku-specific commands.

The app runs as a Django WSGI application on Gunicorn. Heroku Postgres is
required for production data because Heroku dyno filesystems, including
SQLite files, are ephemeral.

## 1. Create the Heroku app and database

1. Install the Heroku CLI and sign in:

   ```bash
   heroku login
   ```

   The live app is named `fire-restaurant-583481b558bc`. Connect its Git
   remote:

   ```bash
   heroku git:remote --app fire-restaurant-583481b558bc
   ```

   For a new app instead, create a unique name with
   `heroku create <app-name>` and substitute that name and hostname in the
   remaining commands.

2. In the Heroku Dashboard, attach a Heroku Postgres database to the app.
   Choose an available plan for your account. Heroku sets `DATABASE_URL`
   automatically when the add-on is attached.
3. Pin the app to the Python buildpack (the repository also contains frontend
   Playwright tooling):

   ```bash
   heroku buildpacks:set heroku/python --app fire-restaurant-583481b558bc
   ```

## 2. Set production configuration

Generate a unique Django secret key locally:

```bash
python3 -c "import secrets; print(secrets.token_urlsafe(50))"
```

Set the key and the exact app host/origin in Heroku config vars. The examples
below use the live app name `fire-restaurant-583481b558bc`:

```bash
heroku config:set \
  DJANGO_SECRET_KEY='paste-the-generated-secret-here' \
  DJANGO_DEBUG=false \
  DJANGO_ALLOWED_HOSTS='fire-restaurant-583481b558bc.herokuapp.com' \
  DJANGO_CSRF_TRUSTED_ORIGINS='https://fire-restaurant-583481b558bc.herokuapp.com' \
  --app fire-restaurant-583481b558bc
```

Do not commit the secret key or local SQLite database. The Django secure
cookies, HTTPS redirect, and proxy settings are configured for Heroku's TLS
router. The release phase in `Procfile` applies migrations against Postgres.
The Python build process collects Django static files, which WhiteNoise serves.

## 3. Deploy

Commit and push the deployment files and application changes to the branch
connected to Heroku. With the Heroku Git remote, deploy the current branch:

```bash
git push heroku HEAD:main
```

If the app is connected to GitHub, push the branch and deploy it from the
Heroku Dashboard instead. Check the deploy and release logs:

```bash
heroku logs --tail --app fire-restaurant-583481b558bc
```

The `release` process runs `python manage.py migrate` against Postgres before
the new release serves traffic. After deployment, confirm migrations and run
the system check:

```bash
heroku run --app fire-restaurant-583481b558bc python manage.py showmigrations --plan
heroku run --app fire-restaurant-583481b558bc python manage.py check
```

## 4. Create a management account

Production starts with a clean Postgres database; it does not receive the local
`database.db` or its `Admin` account. Create a new strong, unique superuser
after deploying:

```bash
heroku run --app fire-restaurant-583481b558bc python manage.py createsuperuser
```

Use `/admin/` to edit menu items and manage reservations and tables. Customer
registration is available at `/accounts/register/`.

## 5. Verify

- Homepage: `https://fire-restaurant-583481b558bc.herokuapp.com/`
- Health: `https://fire-restaurant-583481b558bc.herokuapp.com/api/health`
- Admin: `https://fire-restaurant-583481b558bc.herokuapp.com/admin/`
- Customer registration: `https://fire-restaurant-583481b558bc.herokuapp.com/accounts/register/`

The first migration creates the Django schema and seeds twenty four-seat
restaurant tables. Existing local SQLite customers, reservations, and menu
records are not copied to Postgres; migrate any data that should be retained
using a separate, reviewed data-transfer procedure.
