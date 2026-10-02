from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone


class Customer(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="restaurant_customer",
        null=True,
        blank=True,
    )
    name = models.CharField(max_length=150)
    email = models.EmailField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name", "email"]

    def __str__(self):
        return f"{self.name} ({self.email})"


class Reservation(models.Model):
    table = models.ForeignKey(
        "RestaurantTable",
        on_delete=models.PROTECT,
        related_name="reservations",
    )
    customer = models.ForeignKey(
        Customer,
        on_delete=models.PROTECT,
        related_name="reservations",
    )
    name = models.CharField(max_length=150)
    email = models.EmailField()
    date = models.DateField()
    time = models.TimeField()
    guests = models.PositiveSmallIntegerField()
    requests = models.TextField(blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=30, default="confirmed")

    class Meta:
        db_table = "reservations"
        ordering = ["-date", "-time"]
        constraints = [
            models.UniqueConstraint(
                fields=["table", "date", "time"],
                name="unique_table_reservation_slot",
            ),
            models.UniqueConstraint(
                fields=["customer", "date", "time"],
                name="unique_customer_reservation_slot",
            ),
        ]

    def clean(self):
        if self.date and self.date < timezone.localdate():
            raise ValidationError({"date": "Reservations cannot be made for past dates."})
        if (
            self.date == timezone.localdate()
            and self.time
            and self.time <= timezone.localtime().time().replace(second=0, microsecond=0)
        ):
            raise ValidationError({"time": "Reservations cannot be made for past times."})
        if self.table_id and self.guests and self.guests > self.table.seats:
            raise ValidationError({"guests": "The selected table does not have enough seats."})


class RestaurantTable(models.Model):
    table_number = models.PositiveSmallIntegerField(unique=True)
    seats = models.PositiveSmallIntegerField(default=4)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["table_number"]

    def __str__(self):
        return f"Table {self.table_number} ({self.seats} seats)"


class NewsletterSignup(models.Model):
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=30, default="subscribed")

    class Meta:
        db_table = "newsletter_signups"
        ordering = ["-created_at"]


class MenuItem(models.Model):
    name = models.CharField(max_length=150)
    category = models.CharField(max_length=100)
    description = models.TextField(blank=True, default="")
    price = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    image = models.CharField(max_length=500, blank=True, default="")
    is_chefs_pick = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "menu_items"
        ordering = ["-is_chefs_pick", "name"]
