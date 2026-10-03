# Django API Quick Start

## Requirements

- Python 3.10 or later
- pip

## Install and run

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate --fake-initial
python manage.py runserver 0.0.0.0:5000
```

Local development uses SQLite at `database.db`. Migrations create the schema
and can adopt compatible existing tables through Django's initial-migration
handling. Production requires PostgreSQL configured through `DATABASE_URL`;
the Heroku release phase applies migrations before serving traffic.

- Website: `http://localhost:5000/`
- Health check: `http://localhost:5000/api/health`
- API documentation: `http://localhost:5000/api/docs`
- Django admin/login: `http://localhost:5000/admin/`
- Customer registration: `http://localhost:5000/accounts/register/`
- Customer login: `http://localhost:5000/accounts/login/`
- Reservation dashboard: `http://localhost:5000/reservations/`

## Customer accounts and reservations

Register or log in through the customer pages, then use the reservation
dashboard to view available tables and create, edit, or delete your own
reservations. The database is seeded with 20 tables, each seating four guests.
Customers may book at most four guests per table. Past dates/times, another
customer's table slot, and duplicate date/time bookings for the same customer
are rejected.

The API uses the same Django session. `GET /api/reservations/availability`
requires a logged-in customer and takes `date`, `time`, and `guests` parameters.
`POST /api/reservations` requires a session and accepts a table ID plus date,
time, guest count, and optional requests. `PUT` and `DELETE` on
`/api/reservations/<id>` are limited to the reservation owner (or staff).

## Create a staff account

In a second terminal with the virtual environment activated:

```bash
python manage.py createsuperuser
```

The Django admin login provides staff access to management features. Public
users can subscribe to the newsletter and read menu items.

## Main API routes

### Reservations

- `GET /api/reservations/availability?date=YYYY-MM-DD&time=HH:MM&guests=2` — show availability (login required; pass `reservation=<id>` when editing that reservation)
- `POST /api/reservations` — create for the logged-in customer
- `GET /api/reservations` — list own reservations (staff see all)
- `GET`, `PUT`, `DELETE /api/reservations/<id>` — manage an owned reservation (staff may manage all)

Past dates and times are rejected. The database enforces one reservation per
table/date/time, so simultaneous attempts to book the same slot cannot both
succeed.

### Newsletter

- `POST /api/newsletter/signup` — subscribe an email address
- `GET /api/newsletter/signups` — list subscribers (staff only)

### Menu

- `GET /api/menu` — list items; add `?category=dinner` to filter
- `GET /api/menu/<id>` — retrieve an item
- `POST /api/menu` — create an item (staff only)
- `PUT /api/menu/<id>` — update an item (staff only)
- `DELETE /api/menu/<id>` — delete an item (staff only)

## Example requests

```bash
curl http://localhost:5000/api/health

curl -X POST http://localhost:5000/api/reservations \
  -H "Content-Type: application/json" \
  -d '{"table":1,"date":"2027-01-15","time":"19:30","guests":4}'

curl "http://localhost:5000/api/menu?category=dinner"
```

Run backend tests with `python manage.py test restaurant`.

Reservation API mutations require a logged-in Django customer session and a
valid CSRF token. The customer dashboard is the simplest browser-based way to
register, log in, and manage bookings.
