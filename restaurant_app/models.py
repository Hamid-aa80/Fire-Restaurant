from __future__ import annotations

from django.db import models


class Customer(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'customers'

    def __str__(self) -> str:
        return self.name


class Reservation(models.Model):
    STATUS_CHOICES = [
        ('confirmed', 'Confirmed'),
        ('pending', 'Pending'),
        ('cancelled', 'Cancelled'),
    ]

    name = models.CharField(max_length=200)
    email = models.EmailField()
    date = models.DateField()
    time = models.TimeField(default='19:30')
    guests = models.PositiveIntegerField()
    requests = models.TextField(blank=True, default='')
    customer = models.ForeignKey(
        Customer,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='reservations',
    )
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='confirmed')

    class Meta:
        db_table = 'reservations'

    def __str__(self) -> str:
        return f'{self.name} - {self.date}'


class NewsletterSignup(models.Model):
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default='subscribed')

    class Meta:
        db_table = 'newsletter_signups'

    def __str__(self) -> str:
        return self.email


class MenuItem(models.Model):
    name = models.CharField(max_length=200)
    category = models.CharField(max_length=100)
    description = models.TextField(blank=True, default='')
    price = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    image = models.URLField(blank=True, default='')
    is_chefs_pick = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'menu_items'

    def __str__(self) -> str:
        return self.name
