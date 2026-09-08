from __future__ import annotations

from django.core.management.base import BaseCommand

from python.restaurant_data import sample_menu, sample_reservations
from restaurant_app.models import Customer, MenuItem, NewsletterSignup, Reservation


class Command(BaseCommand):
    help = 'Seed the restaurant database with sample data if it is empty.'

    def handle(self, *args, **options):
        if not MenuItem.objects.exists():
            for item in sample_menu():
                MenuItem.objects.create(**item)
            self.stdout.write(self.style.SUCCESS('Seeded menu items'))

        if not Reservation.objects.exists():
            for reservation in sample_reservations():
                customer, _ = Customer.objects.get_or_create(
                    email=reservation['email'],
                    defaults={'name': reservation['name']},
                )
                Reservation.objects.create(
                    name=reservation['name'],
                    email=reservation['email'],
                    customer=customer,
                    date=reservation['date'],
                    time=reservation['time'],
                    guests=reservation['guests'],
                    requests=reservation.get('requests', ''),
                    status='confirmed',
                )
            self.stdout.write(self.style.SUCCESS('Seeded reservations'))

        if not NewsletterSignup.objects.exists():
            NewsletterSignup.objects.create(email='guest@saltsmoke.example', status='subscribed')
            self.stdout.write(self.style.SUCCESS('Seeded newsletter signup'))
