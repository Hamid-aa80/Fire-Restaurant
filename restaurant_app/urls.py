from django.urls import path

from .views import api_status, menu_list, newsletter_subscribers, reservation_list

urlpatterns = [
    path('', api_status, name='api-status'),
    path('reservations/', reservation_list, name='reservations'),
    path('menu/', menu_list, name='menu'),
    path('newsletter/', newsletter_subscribers, name='newsletter'),
]
