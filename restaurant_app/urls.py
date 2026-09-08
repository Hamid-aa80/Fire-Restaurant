from django.urls import path

from .views import (
    account_page,
    api_status,
    auth_login,
    auth_logout,
    auth_me,
    auth_signup,
    menu_list,
    my_reservations,
    my_reservations_delete,
    newsletter_subscribers,
    reservation_list,
)

urlpatterns = [
    path('', api_status, name='api-status'),
    path('reservations/', reservation_list, name='reservations'),
    path('menu/', menu_list, name='menu'),
    path('newsletter/', newsletter_subscribers, name='newsletter'),
    path('auth/signup', auth_signup, name='auth-signup'),
    path('auth/login', auth_login, name='auth-login'),
    path('auth/logout', auth_logout, name='auth-logout'),
    path('auth/me', auth_me, name='auth-me'),
    path('my/reservations', my_reservations, name='my-reservations'),
    path('my/reservations/<int:reservation_id>', my_reservations_delete, name='my-reservations-delete'),
]
