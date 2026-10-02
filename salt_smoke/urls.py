from pathlib import Path

from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import include, path, re_path
from django.views.static import serve

from restaurant import views
from restaurant.views import homepage, submit_page


PROJECT_ROOT = Path(__file__).resolve().parent.parent

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("restaurant.urls")),
    path("accounts/register/", views.customer_register, name="customer-register"),
    path("accounts/login/", views.customer_login, name="customer-login"),
    path("accounts/logout/", views.customer_logout, name="customer-logout"),
    path(
        "reservations/",
        views.reservation_dashboard,
        name="reservation-dashboard",
    ),
    path(
        "reservations/availability/",
        views.reservation_availability,
        name="reservation-availability",
    ),
    path(
        "reservations/<int:reservation_id>/edit/",
        views.reservation_edit,
        name="reservation-edit",
    ),
    path(
        "reservations/<int:reservation_id>/delete/",
        views.reservation_delete,
        name="reservation-delete",
    ),
    path("", homepage, name="home"),
    path("submit.html", submit_page, name="reservation-confirmation"),
    re_path(
        r"^(?P<path>(?:style\.css|main\.js|assets/img/[A-Za-z0-9_.-]+))$",
        serve,
        {"document_root": str(PROJECT_ROOT)},
    ),
]

urlpatterns += staticfiles_urlpatterns()
