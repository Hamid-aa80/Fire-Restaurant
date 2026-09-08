from django.contrib import admin

from .models import Customer, MenuItem, NewsletterSignup, Reservation


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'created_at')
    search_fields = ('name', 'email')


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('name', 'date', 'time', 'guests', 'status')
    list_filter = ('status', 'date')
    search_fields = ('name', 'email')


@admin.register(NewsletterSignup)
class NewsletterSignupAdmin(admin.ModelAdmin):
    list_display = ('email', 'status', 'created_at')
    search_fields = ('email',)


@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'is_chefs_pick')
    list_filter = ('category', 'is_chefs_pick')
    search_fields = ('name', 'category')
