from __future__ import annotations

from django.http import JsonResponse
from django.views.decorators.http import require_http_methods

from restaurant_app.models import MenuItem, NewsletterSignup, Reservation


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
