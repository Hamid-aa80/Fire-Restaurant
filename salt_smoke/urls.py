import mimetypes
from pathlib import Path

from django.contrib import admin
from django.http import FileResponse, Http404
from django.urls import include, path, re_path

from restaurant import views
from restaurant.views import homepage, submit_page


PROJECT_ROOT = Path(__file__).resolve().parent.parent


def serve_frontend_asset(request, path):
    if path == "style.css":
        asset_path = PROJECT_ROOT / "style.css"
    elif path.startswith("assets/img/"):
        asset_path = PROJECT_ROOT / path
    else:
        raise Http404

    if not asset_path.is_file():
        raise Http404
    content_type, _ = mimetypes.guess_type(asset_path.name)
    return FileResponse(asset_path.open("rb"), content_type=content_type or "application/octet-stream")

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
        r"^(?P<path>(?:style\.css|assets/img/[A-Za-z0-9_.-]+))$",
        serve_frontend_asset,
    ),
]
