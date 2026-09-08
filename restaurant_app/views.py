from __future__ import annotations

import json
import re

from django.contrib.auth.hashers import check_password, make_password
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from restaurant_app.models import Customer, MenuItem, NewsletterSignup, Reservation

EMAIL_RE = re.compile(r'^[^\s@]+@[^\s@]+\.[^\s@]+$')


def _validate_email(email):
    return bool(email) and bool(EMAIL_RE.match(email))


def _validate_signup(data):
    errors = []
    name = (data.get('name') or '').strip()
    email = data.get('email') or ''
    password = data.get('password') or ''

    if len(name) < 2:
        errors.append('Name must be at least 2 characters')
    if not _validate_email(email):
        errors.append('Invalid email format')
    if len(password) < 6:
        errors.append('Password must be at least 6 characters')

    return errors


def _validate_reservation(data):
    errors = []

    if not data.get('date'):
        errors.append('Date is required')
    if not data.get('time'):
        errors.append('Time is required')

    guests = data.get('guests')
    try:
        guests_int = int(guests)
    except (TypeError, ValueError):
        guests_int = None
    if guests_int is None or guests_int < 1 or guests_int > 20:
        errors.append('Guests must be between 1 and 20')

    return errors


def _parse_json_body(request):
    try:
        return json.loads(request.body or '{}')
    except (json.JSONDecodeError, UnicodeDecodeError):
        return {}


def _require_auth(request):
    return request.session.get('customer_id') is not None


@require_http_methods(['GET'])
def api_status(request):
    return JsonResponse({
        'success': True,
        'app': 'Salt & Smoke',
        'status': 'online',
        'framework': 'Django',
    })


@require_http_methods(['GET'])
def reservation_list(request):
    reservations = Reservation.objects.order_by('-date', '-time').all()
    payload = [
        {
            'id': reservation.id,
            'name': reservation.name,
            'email': reservation.email,
            'date': reservation.date.isoformat(),
            'time': reservation.time.isoformat(),
            'guests': reservation.guests,
            'requests': reservation.requests,
            'status': reservation.status,
        }
        for reservation in reservations
    ]
    return JsonResponse({'success': True, 'data': payload})


@require_http_methods(['GET'])
def menu_list(request):
    menu_items = MenuItem.objects.order_by('category', 'name').all()
    payload = [
        {
            'id': item.id,
            'name': item.name,
            'category': item.category,
            'description': item.description,
            'price': float(item.price) if item.price is not None else None,
            'image': item.image,
            'is_chefs_pick': item.is_chefs_pick,
        }
        for item in menu_items
    ]
    return JsonResponse({'success': True, 'data': payload})


@require_http_methods(['GET'])
def newsletter_subscribers(request):
    subscribers = NewsletterSignup.objects.order_by('-created_at').all()
    payload = [
        {
            'id': subscriber.id,
            'email': subscriber.email,
            'status': subscriber.status,
            'created_at': subscriber.created_at.isoformat(),
        }
        for subscriber in subscribers
    ]
    return JsonResponse({'success': True, 'data': payload})


def account_page(request):
    """Renders the sign up / log in / manage-reservations page."""
    return render(request, 'account.html')


@csrf_exempt
@require_http_methods(['POST'])
def auth_signup(request):
    data = _parse_json_body(request)
    errors = _validate_signup(data)
    if errors:
        return JsonResponse({'success': False, 'errors': errors}, status=400)

    name = data['name'].strip()
    email = data['email'].strip().lower()
    password = data['password']

    if Customer.objects.filter(email=email).exists():
        return JsonResponse(
            {'success': False, 'message': 'An account with that email already exists'}, status=400
        )

    customer = Customer.objects.create(
        name=name,
        email=email,
        password_hash=make_password(password),
    )

    request.session['customer_id'] = customer.id
    request.session['customer_name'] = customer.name
    request.session['customer_email'] = customer.email

    return JsonResponse(
        {
            'success': True,
            'message': 'Account created successfully',
            'customer': {'id': customer.id, 'name': customer.name, 'email': customer.email},
        },
        status=201,
    )


@csrf_exempt
@require_http_methods(['POST'])
def auth_login(request):
    data = _parse_json_body(request)
    email = (data.get('email') or '').strip()
    password = data.get('password') or ''

    if not _validate_email(email) or not password:
        return JsonResponse(
            {'success': False, 'message': 'Email and password are required'}, status=400
        )

    normalized_email = email.lower()

    try:
        customer = Customer.objects.get(email=normalized_email)
    except Customer.DoesNotExist:
        customer = None

    if not customer or not customer.password_hash or not check_password(password, customer.password_hash):
        return JsonResponse({'success': False, 'message': 'Invalid email or password'}, status=401)

    request.session['customer_id'] = customer.id
    request.session['customer_name'] = customer.name
    request.session['customer_email'] = customer.email

    return JsonResponse(
        {
            'success': True,
            'message': 'Logged in successfully',
            'customer': {'id': customer.id, 'name': customer.name, 'email': customer.email},
        }
    )


@csrf_exempt
@require_http_methods(['POST'])
def auth_logout(request):
    request.session.flush()
    return JsonResponse({'success': True, 'message': 'Logged out successfully'})


@require_http_methods(['GET'])
def auth_me(request):
    customer_id = request.session.get('customer_id')
    if not customer_id:
        return JsonResponse({'success': True, 'customer': None})

    return JsonResponse(
        {
            'success': True,
            'customer': {
                'id': customer_id,
                'name': request.session.get('customer_name'),
                'email': request.session.get('customer_email'),
            },
        }
    )


@csrf_exempt
@require_http_methods(['GET', 'POST'])
def my_reservations(request):
    if request.method == 'GET':
        return my_reservations_list(request)
    return my_reservations_create(request)


@require_http_methods(['GET'])
def my_reservations_list(request):
    if not _require_auth(request):
        return JsonResponse({'success': False, 'message': 'You must be logged in to do that'}, status=401)

    reservations = Reservation.objects.filter(
        customer_id=request.session['customer_id']
    ).order_by('-date', '-time')
    payload = [
        {
            'id': reservation.id,
            'name': reservation.name,
            'email': reservation.email,
            'date': reservation.date.isoformat(),
            'time': reservation.time.isoformat(timespec='minutes'),
            'guests': reservation.guests,
            'requests': reservation.requests,
            'status': reservation.status,
        }
        for reservation in reservations
    ]
    return JsonResponse({'success': True, 'data': payload})


@csrf_exempt
@require_http_methods(['POST'])
def my_reservations_create(request):
    if not _require_auth(request):
        return JsonResponse({'success': False, 'message': 'You must be logged in to do that'}, status=401)

    data = _parse_json_body(request)
    data.setdefault('time', '19:30')
    errors = _validate_reservation(data)
    if errors:
        return JsonResponse({'success': False, 'errors': errors}, status=400)

    reservation = Reservation.objects.create(
        name=request.session['customer_name'],
        email=request.session['customer_email'],
        date=data['date'],
        time=data['time'],
        guests=int(data['guests']),
        requests=(data.get('requests') or '').strip(),
        customer_id=request.session['customer_id'],
    )

    return JsonResponse(
        {
            'success': True,
            'message': 'Reservation created successfully',
            'reservationId': reservation.id,
        },
        status=201,
    )


@csrf_exempt
@require_http_methods(['DELETE'])
def my_reservations_delete(request, reservation_id):
    if not _require_auth(request):
        return JsonResponse({'success': False, 'message': 'You must be logged in to do that'}, status=401)

    try:
        reservation = Reservation.objects.get(id=reservation_id, customer_id=request.session['customer_id'])
    except Reservation.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Reservation not found'}, status=404)

    reservation.delete()
    return JsonResponse({'success': True, 'message': 'Reservation cancelled successfully'})
