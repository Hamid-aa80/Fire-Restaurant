import json
from datetime import date, time, timedelta
from functools import wraps
from pathlib import Path

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError, transaction
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from .forms import (
    CustomerLoginForm,
    CustomerRegistrationForm,
    MenuItemForm,
    NewsletterSignupForm,
    ReservationAvailabilityForm,
    ReservationForm,
)
from .models import Customer, MenuItem, NewsletterSignup, Reservation, RestaurantTable


def homepage(request):
    content = Path(settings.BASE_DIR, "index.html").read_text(encoding="utf-8")
    return HttpResponse(content)


def submit_page(request):
    content = Path(settings.BASE_DIR, "submit.html").read_text(encoding="utf-8")
    return HttpResponse(content)


def _payload(request):
    if "application/json" not in (request.content_type or "").lower():
        return request.POST.dict()

    try:
        payload = json.loads(request.body)
    except (json.JSONDecodeError, UnicodeDecodeError):
        return None

    return payload if isinstance(payload, dict) else None


def _form_errors(form):
    errors = []
    for field_errors in form.errors.values():
        for error in field_errors:
            errors.append(str(error))
    return errors


def staff_api_required(view):
    @wraps(view)
    def wrapped(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse(
                {"success": False, "message": "Authentication required"},
                status=401,
            )
        if not request.user.is_staff:
            return JsonResponse(
                {"success": False, "message": "Staff access required"},
                status=403,
            )
        return view(request, *args, **kwargs)

    return wrapped


def _reservation_json(reservation):
    return {
        "id": reservation.pk,
        "customerId": reservation.customer_id,
        "tableId": reservation.table_id,
        "tableNumber": reservation.table.table_number,
        "name": reservation.name,
        "email": reservation.email,
        "date": reservation.date.isoformat(),
        "time": reservation.time.strftime("%H:%M"),
        "guests": reservation.guests,
        "requests": reservation.requests,
        "created_at": reservation.created_at.isoformat(),
        "status": reservation.status,
    }


def _customer_for_user(user):
    return Customer.objects.filter(user=user).first()


def _table_availability(reservation_date, reservation_time, guests, exclude=None):
    booked_tables = Reservation.objects.filter(
        date=reservation_date,
        time=reservation_time,
    )
    if exclude is not None:
        booked_tables = booked_tables.exclude(pk=exclude.pk)
    booked_ids = set(booked_tables.values_list("table_id", flat=True))

    return [
        {
            "id": table.pk,
            "table_number": table.table_number,
            "seats": table.seats,
            "available": table.pk not in booked_ids and table.seats >= guests,
        }
        for table in RestaurantTable.objects.filter(is_active=True)
    ]


def _reservation_form_initial(reservation=None):
    if reservation:
        return {
            "date": reservation.date,
            "time": reservation.time.strftime("%H:%M"),
            "guests": reservation.guests,
            "requests": reservation.requests,
            "table": reservation.table_id,
        }
    return {
        "date": timezone.localdate() + timedelta(days=1),
        "time": "19:00",
        "guests": 2,
    }


def _reservation_page_context(form, reservation=None):
    cleaned = getattr(form, "cleaned_data", {})
    initial = getattr(form, "initial", {})
    posted = form.data if form.is_bound else {}
    selected_date = cleaned.get("date") or posted.get("date") or initial.get("date")
    selected_time = cleaned.get("time") or posted.get("time") or initial.get("time")
    guests = cleaned.get("guests") or posted.get("guests") or initial.get("guests") or 2
    if isinstance(selected_time, time):
        selected_time = selected_time.strftime("%H:%M")
    if isinstance(selected_date, date):
        selected_date = selected_date.isoformat()

    tables = []
    if selected_date and selected_time:
        try:
            tables = _table_availability(
                date.fromisoformat(str(selected_date)),
                time.fromisoformat(str(selected_time)),
                int(guests),
                exclude=reservation,
            )
        except (TypeError, ValueError):
            tables = []

    return {
        "form": form,
        "tables": tables,
        "selected_date": selected_date or "",
        "selected_time": selected_time or "",
        "selected_guests": guests,
        "editing": reservation,
        "availability_url": reverse("reservation-availability"),
    }


def customer_register(request):
    if request.user.is_authenticated:
        return redirect("reservation-dashboard")
    form = CustomerRegistrationForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        with transaction.atomic():
            user = form.save()
            Customer.objects.create(
                user=user,
                email=user.email,
                name=user.first_name,
            )
        login(request, user)
        return redirect("reservation-dashboard")
    return render(request, "restaurant/register.html", {"form": form})


def customer_login(request):
    if request.user.is_authenticated:
        return redirect("reservation-dashboard")
    form = CustomerLoginForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = authenticate(
            request,
            username=form.cleaned_data["email"].strip().lower(),
            password=form.cleaned_data["password"],
        )
        if user is None:
            form.add_error(None, "Email or password is incorrect.")
        else:
            login(request, user)
            next_url = request.POST.get("next") or request.GET.get("next")
            if next_url and url_has_allowed_host_and_scheme(
                next_url,
                allowed_hosts={request.get_host()},
                require_https=request.is_secure(),
            ):
                return redirect(next_url)
            return redirect("reservation-dashboard")
    return render(
        request,
        "restaurant/login.html",
        {"form": form, "next": request.GET.get("next", "")},
    )


@require_http_methods(["POST"])
def customer_logout(request):
    logout(request)
    return redirect("customer-login")


@login_required(login_url="customer-login")
@require_http_methods(["GET", "POST"])
def reservation_dashboard(request):
    customer = get_object_or_404(Customer, user=request.user)
    form = ReservationForm(
        request.POST or None,
        customer=customer,
        initial=_reservation_form_initial(),
    )
    if request.method == "POST" and form.is_valid():
        reservation_data = form.cleaned_data
        try:
            with transaction.atomic():
                Reservation.objects.create(
                    customer=customer,
                    table=reservation_data["table"],
                    name=customer.name,
                    email=customer.email,
                    date=reservation_data["date"],
                    time=reservation_data["time"],
                    guests=reservation_data["guests"],
                    requests=reservation_data["requests"],
                )
        except IntegrityError:
            form.add_error(None, "That table or time was just booked. Please choose another.")
        else:
            messages.success(request, "Your reservation has been created.")
            return redirect("reservation-dashboard")

    context = _reservation_page_context(form)
    context["reservations"] = Reservation.objects.filter(customer=customer).select_related("table")
    context["customer"] = customer
    return render(request, "restaurant/reservations.html", context)


@login_required(login_url="customer-login")
@require_http_methods(["GET", "POST"])
def reservation_edit(request, reservation_id):
    customer = get_object_or_404(Customer, user=request.user)
    reservation = get_object_or_404(
        Reservation.objects.select_related("table", "customer"),
        pk=reservation_id,
        customer=customer,
    )
    form = ReservationForm(
        request.POST or None,
        customer=customer,
        reservation=reservation,
        initial=_reservation_form_initial(reservation),
    )
    if request.method == "POST" and form.is_valid():
        reservation_data = form.cleaned_data
        reservation.table = reservation_data["table"]
        reservation.date = reservation_data["date"]
        reservation.time = reservation_data["time"]
        reservation.guests = reservation_data["guests"]
        reservation.requests = reservation_data["requests"]
        try:
            with transaction.atomic():
                reservation.save(
                    update_fields=["table", "date", "time", "guests", "requests"]
                )
        except IntegrityError:
            form.add_error(None, "That table or time was just booked. Please choose another.")
        else:
            messages.success(request, "Your reservation has been updated.")
            return redirect("reservation-dashboard")

    context = _reservation_page_context(form, reservation)
    context["reservations"] = None
    context["customer"] = customer
    return render(request, "restaurant/reservations.html", context)


@login_required(login_url="customer-login")
@require_http_methods(["POST"])
def reservation_delete(request, reservation_id):
    customer = get_object_or_404(Customer, user=request.user)
    reservation = get_object_or_404(
        Reservation,
        pk=reservation_id,
        customer=customer,
    )
    reservation.delete()
    messages.success(request, "Your reservation has been cancelled.")
    return redirect("reservation-dashboard")


@login_required(login_url="customer-login")
@require_http_methods(["GET"])
def reservation_availability(request):
    customer = get_object_or_404(Customer, user=request.user)
    form = ReservationAvailabilityForm(request.GET)
    if not form.is_valid():
        return JsonResponse(
            {"success": False, "errors": _form_errors(form)},
            status=400,
        )
    tables = _table_availability(
        form.cleaned_data["date"],
        form.cleaned_data["time"],
        form.cleaned_data["guests"],
    )
    return JsonResponse(
        {
            "success": True,
            "tables": tables,
            "availableCount": sum(table["available"] for table in tables),
            "customerId": customer.pk,
        }
    )

def _signup_json(signup):
    return {
        "id": signup.pk,
        "email": signup.email,
        "created_at": signup.created_at.isoformat(),
        "status": signup.status,
    }


def _menu_item_json(item):
    return {
        "id": item.pk,
        "name": item.name,
        "category": item.category,
        "description": item.description,
        "price": float(item.price) if item.price is not None else None,
        "image": item.image,
        "is_chefs_pick": int(item.is_chefs_pick),
        "created_at": item.created_at.isoformat(),
    }


def health(request):
    return JsonResponse({"status": "API is running"})


def api_docs(request):
    documentation = Path(settings.BASE_DIR, "API-DOCUMENTATION.md").read_text(encoding="utf-8")
    return HttpResponse(documentation, content_type="text/markdown; charset=utf-8")


@require_http_methods(["GET", "POST"])
def reservations(request):
    if request.method == "GET":
        if not request.user.is_authenticated:
            return JsonResponse(
                {"success": False, "message": "Authentication required"},
                status=401,
            )
        bookings = Reservation.objects.select_related("customer", "table")
        if not request.user.is_staff:
            customer = _customer_for_user(request.user)
            if customer is None:
                return JsonResponse(
                    {"success": False, "message": "Customer account required"},
                    status=403,
                )
            bookings = bookings.filter(customer=customer)
        data = [_reservation_json(row) for row in bookings]
        return JsonResponse({"success": True, "data": data})

    if not request.user.is_authenticated:
        return JsonResponse(
            {"success": False, "message": "Authentication required"},
            status=401,
        )
    customer = _customer_for_user(request.user)
    if customer is None:
        return JsonResponse(
            {"success": False, "message": "Customer account required"},
            status=403,
        )
    payload = _payload(request)
    if payload is None:
        return JsonResponse(
            {"success": False, "errors": ["Request body must be a JSON object"]},
            status=400,
        )
    form = ReservationForm(payload, customer=customer)
    if not form.is_valid():
        return JsonResponse({"success": False, "errors": _form_errors(form)}, status=400)

    reservation_data = form.cleaned_data
    try:
        with transaction.atomic():
            reservation = Reservation.objects.create(
                customer=customer,
                table=reservation_data["table"],
                name=customer.name,
                email=customer.email,
                date=reservation_data["date"],
                time=reservation_data["time"],
                guests=reservation_data["guests"],
                requests=reservation_data["requests"],
            )
    except IntegrityError:
        return JsonResponse(
            {
                "success": False,
                "message": "That table or time was just booked. Please choose another.",
            },
            status=409,
        )
    return JsonResponse(
        {
            "success": True,
            "message": "Reservation created successfully",
            "reservationId": reservation.pk,
        },
        status=201,
    )


@require_http_methods(["GET", "PUT", "DELETE"])
def reservation_detail(request, reservation_id):
    if not request.user.is_authenticated:
        return JsonResponse(
            {"success": False, "message": "Authentication required"},
            status=401,
        )
    reservation = Reservation.objects.select_related("customer", "table").filter(
        pk=reservation_id
    ).first()
    if reservation is None:
        return JsonResponse(
            {"success": False, "message": "Reservation not found"},
            status=404,
        )
    if not request.user.is_staff:
        customer = _customer_for_user(request.user)
        if customer is None or reservation.customer_id != customer.pk:
            return JsonResponse(
                {"success": False, "message": "Reservation not found"},
                status=404,
            )

    if request.method == "GET":
        return JsonResponse({"success": True, "data": _reservation_json(reservation)})
    if request.method == "DELETE":
        reservation.delete()
        return JsonResponse({"success": True, "message": "Reservation deleted successfully"})

    payload = _payload(request)
    if payload is None:
        return JsonResponse(
            {"success": False, "errors": ["Request body must be a JSON object"]},
            status=400,
        )
    form = ReservationForm(
        payload,
        customer=reservation.customer,
        reservation=reservation,
    )
    if not form.is_valid():
        return JsonResponse({"success": False, "errors": _form_errors(form)}, status=400)

    reservation_data = form.cleaned_data
    reservation.table = reservation_data["table"]
    reservation.date = reservation_data["date"]
    reservation.time = reservation_data["time"]
    reservation.guests = reservation_data["guests"]
    reservation.requests = reservation_data["requests"]
    try:
        with transaction.atomic():
            reservation.save(update_fields=["table", "date", "time", "guests", "requests"])
    except IntegrityError:
        return JsonResponse(
            {
                "success": False,
                "message": "That table or time was just booked. Please choose another.",
            },
            status=409,
        )
    return JsonResponse({"success": True, "message": "Reservation updated successfully"})


@require_http_methods(["GET"])
def reservation_availability_api(request):
    if not request.user.is_authenticated:
        return JsonResponse(
            {"success": False, "message": "Authentication required"},
            status=401,
        )
    if not request.user.is_staff and _customer_for_user(request.user) is None:
        return JsonResponse(
            {"success": False, "message": "Customer account required"},
            status=403,
        )
    form = ReservationAvailabilityForm(request.GET)
    if not form.is_valid():
        return JsonResponse(
            {"success": False, "errors": _form_errors(form)},
            status=400,
        )
    tables = _table_availability(
        form.cleaned_data["date"],
        form.cleaned_data["time"],
        form.cleaned_data["guests"],
    )
    return JsonResponse(
        {
            "success": True,
            "tables": tables,
            "availableCount": sum(table["available"] for table in tables),
        }
    )


@csrf_exempt
@require_http_methods(["POST"])
def newsletter_signup(request):
    payload = _payload(request)
    if payload is None:
        return JsonResponse(
            {"success": False, "message": "Request body must be a JSON object"},
            status=400,
        )
    form = NewsletterSignupForm(payload)
    if not form.is_valid():
        return JsonResponse(
            {"success": False, "message": "Invalid email format"},
            status=400,
        )

    email = form.cleaned_data["email"]
    if NewsletterSignup.objects.filter(email=email).exists():
        return JsonResponse(
            {"success": False, "message": "Email already subscribed"},
            status=400,
        )
    try:
        with transaction.atomic():
            signup = NewsletterSignup.objects.create(email=email)
    except IntegrityError:
        return JsonResponse(
            {"success": False, "message": "Email already subscribed"},
            status=400,
        )
    return JsonResponse(
        {
            "success": True,
            "message": "Successfully subscribed to newsletter",
            "signupId": signup.pk,
        },
        status=201,
    )


@staff_api_required
@require_http_methods(["GET"])
def newsletter_signups(request):
    data = [_signup_json(row) for row in NewsletterSignup.objects.all()]
    return JsonResponse({"success": True, "data": data})


@require_http_methods(["GET", "POST"])
def menu_items(request):
    if request.method == "GET":
        items = MenuItem.objects.all()
        category = request.GET.get("category")
        if category:
            items = items.filter(category=category)
        data = [_menu_item_json(item) for item in items]
        return JsonResponse({"success": True, "data": data})

    if not request.user.is_authenticated or not request.user.is_staff:
        return JsonResponse(
            {"success": False, "message": "Staff authentication required"},
            status=401 if not request.user.is_authenticated else 403,
        )
    payload = _payload(request)
    if payload is None:
        return JsonResponse(
            {"success": False, "errors": ["Request body must be a JSON object"]},
            status=400,
        )
    form = MenuItemForm(payload)
    if not form.is_valid():
        return JsonResponse({"success": False, "errors": _form_errors(form)}, status=400)

    item = MenuItem.objects.create(**form.cleaned_data)
    return JsonResponse(
        {
            "success": True,
            "message": "Menu item created successfully",
            "menuId": item.pk,
        },
        status=201,
    )


@require_http_methods(["GET", "PUT", "DELETE"])
def menu_item_detail(request, item_id):
    if request.method != "GET" and (
        not request.user.is_authenticated or not request.user.is_staff
    ):
        return JsonResponse(
            {"success": False, "message": "Staff authentication required"},
            status=401 if not request.user.is_authenticated else 403,
        )

    item = MenuItem.objects.filter(pk=item_id).first()
    if item is None:
        return JsonResponse(
            {"success": False, "message": "Menu item not found"},
            status=404,
        )

    if request.method == "GET":
        return JsonResponse({"success": True, "data": _menu_item_json(item)})
    if request.method == "DELETE":
        item.delete()
        return JsonResponse({"success": True, "message": "Menu item deleted successfully"})

    payload = _payload(request)
    if payload is None:
        return JsonResponse(
            {"success": False, "errors": ["Request body must be a JSON object"]},
            status=400,
        )
    form = MenuItemForm(payload)
    if not form.is_valid():
        return JsonResponse({"success": False, "errors": _form_errors(form)}, status=400)

    for field, value in form.cleaned_data.items():
        setattr(item, field, value)
    item.save()
    return JsonResponse({"success": True, "message": "Menu item updated successfully"})
