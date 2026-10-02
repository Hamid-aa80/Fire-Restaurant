import json
from datetime import timedelta

from django.contrib.auth import get_user_model
from django.db.models.deletion import ProtectedError
from django.test import Client, TestCase
from django.test.utils import override_settings
from django.urls import reverse
from django.utils import timezone

from .models import Customer, MenuItem, NewsletterSignup, Reservation, RestaurantTable


class CustomerApiTests(TestCase):
    def setUp(self):
        self.user, self.customer = self.create_customer(
            "taylor@example.com",
            "Taylor Guest",
        )
        self.client.force_login(self.user)

    def create_customer(self, email, name):
        user = get_user_model().objects.create_user(
            username=email,
            email=email,
            first_name=name,
            password="a-secure-test-password",
        )
        customer = Customer.objects.create(user=user, name=name, email=email)
        return user, customer

    def reservation_payload(self, **overrides):
        payload = {
            "date": (timezone.localdate() + timedelta(days=2)).isoformat(),
            "time": "19:30",
            "guests": 4,
            "requests": "Window seat",
            "table": RestaurantTable.objects.get(table_number=1).pk,
        }
        payload.update(overrides)
        return payload

    def create_reservation(self, payload=None, client=None):
        return (client or self.client).post(
            reverse("reservations"),
            data=json.dumps(payload or self.reservation_payload()),
            content_type="application/json",
        )

    def test_health_and_frontend_routes(self):
        self.assertEqual(
            self.client.get(reverse("api-health")).json(),
            {"status": "API is running"},
        )
        self.assertContains(self.client.get(reverse("home")), "<title>Fire_Restaurant</title>")

    @override_settings(DEBUG=False, SECURE_SSL_REDIRECT=False)
    def test_frontend_assets_are_served_in_production_mode(self):
        css = self.client.get("/style.css")
        image = self.client.get("/assets/img/favicon.svg")

        self.assertEqual(css.status_code, 200)
        self.assertEqual(css["Content-Type"], "text/css")
        self.assertEqual(image.status_code, 200)
        self.assertEqual(image["Content-Type"], "image/svg+xml")

    def test_reservation_creation_uses_authenticated_customer_identity(self):
        response = self.create_reservation(
            self.reservation_payload(name="Forged Name", email="forged@example.com")
        )

        self.assertEqual(response.status_code, 201)
        reservation = Reservation.objects.select_related("customer", "table").get()
        self.assertEqual(reservation.customer, self.customer)
        self.assertEqual(reservation.name, self.customer.name)
        self.assertEqual(reservation.email, self.customer.email)
        self.assertEqual(reservation.table.table_number, 1)

    def test_customer_can_have_multiple_reservations(self):
        for days in (2, 3):
            response = self.create_reservation(
                self.reservation_payload(
                    date=(timezone.localdate() + timedelta(days=days)).isoformat(),
                )
            )
            self.assertEqual(response.status_code, 201)

        self.assertEqual(Customer.objects.count(), 1)
        self.assertEqual(self.customer.reservations.count(), 2)
        result = self.client.get(reverse("reservations")).json()["data"]
        self.assertEqual({item["customerId"] for item in result}, {self.customer.pk})

    def test_customer_with_reservations_cannot_be_deleted(self):
        Reservation.objects.create(
            customer=self.customer,
            table=RestaurantTable.objects.first(),
            name=self.customer.name,
            email=self.customer.email,
            date=timezone.localdate() + timedelta(days=2),
            time="19:30",
            guests=2,
        )
        with self.assertRaises(ProtectedError):
            self.customer.delete()

    def test_anonymous_users_cannot_book_or_view_reservations(self):
        anonymous_client = Client()
        self.assertEqual(
            self.create_reservation(client=anonymous_client).status_code,
            401,
        )
        self.assertEqual(
            anonymous_client.get(reverse("reservations")).status_code,
            401,
        )
        self.assertEqual(
            anonymous_client.get(reverse("reservation-dashboard")).status_code,
            302,
        )

    def test_availability_displays_all_twenty_tables(self):
        self.assertEqual(RestaurantTable.objects.count(), 20)
        response = self.client.get(
            reverse("api-reservation-availability"),
            {
                "date": (timezone.localdate() + timedelta(days=2)).isoformat(),
                "time": "19:30",
                "guests": 4,
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["availableCount"], 20)
        self.assertEqual(len(response.json()["tables"]), 20)
        self.assertEqual({table["seats"] for table in response.json()["tables"]}, {4})

    def test_table_slot_and_customer_duplicate_slots_are_rejected(self):
        payload = self.reservation_payload()
        self.assertEqual(self.create_reservation(payload).status_code, 201)

        other_user, _ = self.create_customer("other@example.com", "Other Guest")
        self.client.force_login(other_user)
        table_conflict = self.create_reservation(payload)
        self.assertEqual(table_conflict.status_code, 400)

        self.client.force_login(self.user)
        customer_conflict = self.create_reservation(
            self.reservation_payload(table=RestaurantTable.objects.get(table_number=2).pk)
        )
        self.assertEqual(customer_conflict.status_code, 400)
        self.assertEqual(Reservation.objects.count(), 1)

    def test_past_date_time_and_parties_over_four_are_rejected(self):
        past_date = self.create_reservation(
            self.reservation_payload(
                date=(timezone.localdate() - timedelta(days=1)).isoformat()
            )
        )
        too_many_guests = self.create_reservation(self.reservation_payload(guests=5))
        self.assertEqual(past_date.status_code, 400)
        self.assertEqual(too_many_guests.status_code, 400)

        if timezone.localtime().time().hour > 0:
            past_time = self.create_reservation(
                self.reservation_payload(
                    date=timezone.localdate().isoformat(),
                    time="00:01",
                )
            )
            self.assertEqual(past_time.status_code, 400)
        self.assertEqual(Reservation.objects.count(), 0)

    def test_customer_can_edit_and_delete_only_their_own_reservations(self):
        created = self.create_reservation()
        reservation_id = created.json()["reservationId"]
        detail_url = reverse("reservation-detail", args=[reservation_id])
        updated = self.client.put(
            detail_url,
            data=json.dumps(
                self.reservation_payload(
                    date=(timezone.localdate() + timedelta(days=4)).isoformat(),
                    table=RestaurantTable.objects.get(table_number=2).pk,
                    guests=2,
                    requests="Birthday",
                )
            ),
            content_type="application/json",
        )
        self.assertEqual(updated.status_code, 200)
        reservation = Reservation.objects.get(pk=reservation_id)
        self.assertEqual(reservation.table.table_number, 2)
        self.assertEqual(reservation.requests, "Birthday")

        other_user, _ = self.create_customer("other@example.com", "Other Guest")
        self.client.force_login(other_user)
        self.assertEqual(self.client.get(detail_url).status_code, 404)
        self.assertEqual(self.client.delete(detail_url).status_code, 404)

        self.client.force_login(self.user)
        self.assertEqual(self.client.delete(detail_url).status_code, 200)
        self.assertFalse(Reservation.objects.filter(pk=reservation_id).exists())

    def test_customer_registration_login_and_dashboard(self):
        client = Client()
        registration = client.post(
            reverse("customer-register"),
            {
                "name": "Morgan Guest",
                "email": "morgan@example.com",
                "password1": "A-strong-test-password-2026",
                "password2": "A-strong-test-password-2026",
            },
        )
        self.assertRedirects(registration, reverse("reservation-dashboard"))
        customer = Customer.objects.get(email="morgan@example.com")
        self.assertEqual(customer.user.email, "morgan@example.com")
        self.assertEqual(client.get(reverse("reservation-dashboard")).status_code, 200)

        client.post(reverse("customer-logout"))
        login_response = client.post(
            reverse("customer-login"),
            {
                "email": "morgan@example.com",
                "password": "A-strong-test-password-2026",
            },
        )
        self.assertRedirects(login_response, reverse("reservation-dashboard"))
        dashboard = client.get(reverse("reservation-dashboard"))
        self.assertContains(dashboard, "Table 1")
        self.assertContains(dashboard, "Table 20")

    def test_registration_does_not_claim_legacy_reservations_by_email(self):
        legacy_customer = Customer.objects.create(
            name="Legacy Taylor",
            email="claim@example.com",
        )
        Reservation.objects.create(
            customer=legacy_customer,
            table=RestaurantTable.objects.first(),
            name=legacy_customer.name,
            email=legacy_customer.email,
            date=timezone.localdate() + timedelta(days=2),
            time="17:00",
            guests=2,
        )
        response = Client().post(
            reverse("customer-register"),
            {
                "name": "Taylor Claim",
                "email": "claim@example.com",
                "password1": "A-strong-test-password-2026",
                "password2": "A-strong-test-password-2026",
            },
        )
        self.assertRedirects(response, reverse("reservation-dashboard"))
        self.assertEqual(Customer.objects.filter(email="claim@example.com").count(), 2)
        registered_customer = Customer.objects.get(user__email="claim@example.com")
        self.assertEqual(registered_customer.name, "Taylor Claim")
        self.assertEqual(registered_customer.reservations.count(), 0)
        self.assertEqual(legacy_customer.reservations.count(), 1)

    def test_reservation_dashboard_supports_create_edit_and_delete(self):
        dashboard_url = reverse("reservation-dashboard")
        date = (timezone.localdate() + timedelta(days=2)).isoformat()
        created = self.client.post(
            dashboard_url,
            {
                "date": date,
                "time": "18:30",
                "guests": 2,
                "requests": "Anniversary",
                "table": RestaurantTable.objects.get(table_number=1).pk,
            },
        )
        self.assertRedirects(created, dashboard_url)
        reservation = Reservation.objects.get()

        edit_url = reverse("reservation-edit", args=[reservation.pk])
        changed_date = (timezone.localdate() + timedelta(days=3)).isoformat()
        updated = self.client.post(
            edit_url,
            {
                "date": changed_date,
                "time": "19:00",
                "guests": 3,
                "requests": "Birthday",
                "table": RestaurantTable.objects.get(table_number=2).pk,
            },
        )
        self.assertRedirects(updated, dashboard_url)
        reservation.refresh_from_db()
        self.assertEqual(reservation.date.isoformat(), changed_date)
        self.assertEqual(reservation.table.table_number, 2)
        self.assertEqual(reservation.requests, "Birthday")

        deleted = self.client.post(reverse("reservation-delete", args=[reservation.pk]))
        self.assertRedirects(deleted, dashboard_url)
        self.assertFalse(Reservation.objects.exists())

    def test_invalid_json_is_reported_as_a_client_error(self):
        response = self.client.post(
            reverse("reservations"),
            data="{invalid json",
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json()["errors"],
            ["Request body must be a JSON object"],
        )

    def test_newsletter_signup_rejects_invalid_and_duplicate_emails(self):
        url = reverse("newsletter-signup")
        invalid = self.client.post(
            url,
            data=json.dumps({"email": "invalid"}),
            content_type="application/json",
        )
        payload = json.dumps({"email": "guest@example.com"})
        created = self.client.post(url, data=payload, content_type="application/json")
        duplicate = self.client.post(url, data=payload, content_type="application/json")
        self.assertEqual(invalid.status_code, 400)
        self.assertEqual(created.status_code, 201)
        self.assertEqual(duplicate.status_code, 400)
        self.assertEqual(NewsletterSignup.objects.count(), 1)

    def test_menu_is_public_to_read_and_can_be_filtered(self):
        MenuItem.objects.create(name="Brisket", category="dinner", price="24.99")
        MenuItem.objects.create(name="Coffee", category="drinks", price="3.50")
        response = self.client.get(reverse("menu-items"), {"category": "dinner"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual([item["name"] for item in response.json()["data"]], ["Brisket"])


class StaffApiTests(TestCase):
    def setUp(self):
        self.staff_user = get_user_model().objects.create_user(
            username="restaurant-manager",
            password="a-secure-test-password",
            is_staff=True,
        )

    def test_staff_menu_management_requires_staff_authentication(self):
        self.assertEqual(self.client.get(reverse("newsletter-signups")).status_code, 401)
        self.client.force_login(self.staff_user)
        response = self.client.post(
            reverse("menu-items"),
            data=json.dumps(
                {
                    "name": "Smoked Brisket",
                    "category": "dinner",
                    "description": "Slow smoked",
                    "price": 24.99,
                    "is_chefs_pick": True,
                }
            ),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 201)
        item_id = response.json()["menuId"]
        self.assertEqual(
            self.client.delete(reverse("menu-item-detail", args=[item_id])).status_code,
            200,
        )

    def test_django_admin_allows_staff_to_create_and_edit_menu_items(self):
        admin_user = get_user_model().objects.create_superuser(
            username="menu-admin",
            email="admin@example.com",
            password="a-secure-admin-test-password",
        )
        self.client.force_login(admin_user)
        add_page = self.client.get("/admin/restaurant/menuitem/add/")
        self.assertEqual(add_page.status_code, 200)

        created = self.client.post(
            "/admin/restaurant/menuitem/add/",
            {
                "name": "Smoked Ribs",
                "category": "dinner",
                "description": "Slow-cooked ribs",
                "price": "22.50",
                "image": "",
                "is_chefs_pick": "on",
                "_save": "Save",
            },
            follow=True,
        )
        self.assertEqual(created.status_code, 200)
        item = MenuItem.objects.get(name="Smoked Ribs")
        self.assertTrue(item.is_chefs_pick)

        edit_page = self.client.get(f"/admin/restaurant/menuitem/{item.pk}/change/")
        self.assertEqual(edit_page.status_code, 200)
