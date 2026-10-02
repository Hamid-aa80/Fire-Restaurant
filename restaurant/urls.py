from django.urls import path

from . import views


urlpatterns = [
    path("health", views.health, name="api-health"),
    path("docs", views.api_docs, name="api-docs"),
    path("reservations/availability", views.reservation_availability_api, name="api-reservation-availability"),
    path("reservations", views.reservations, name="reservations"),
    path("reservations/<int:reservation_id>", views.reservation_detail, name="reservation-detail"),
    path("newsletter/signup", views.newsletter_signup, name="newsletter-signup"),
    path("newsletter/signups", views.newsletter_signups, name="newsletter-signups"),
    path("menu", views.menu_items, name="menu-items"),
    path("menu/<int:item_id>", views.menu_item_detail, name="menu-item-detail"),
]
