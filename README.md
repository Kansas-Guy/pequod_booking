# Green Mountain Falls Cabin Booking

Simple Airbnb-style internal family booking site built with Django.

## Features
- Family login with Django auth
- Monday-first visual year calendar
- Booking form with overlap prevention
- Same-day bookings supported
- Automatic amount due based on `$25/night`
- Venmo payment link for easy checkout
- Admin panel for one admin user to manage bookings

## Quick start
```bash
python -m venv .venv
source .venv/bin/activate
pip install django
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Then visit:
- App: http://127.0.0.1:8000/
- Admin: http://127.0.0.1:8000/admin/

## Settings to customize
In `cabin_booking/settings.py` update:
- `CABIN_NIGHTLY_RATE`
- `CABIN_VENMO_HANDLE`
