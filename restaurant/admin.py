from django.contrib import admin

from .models import Customer, MenuItem, NewsletterSignup, Reservation, RestaurantTable


class ReservationInline(admin.TabularInline):
    model = Reservation
    extra = 0


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "created_at")
    search_fields = ("name", "email")
    inlines = (ReservationInline,)


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "table", "date", "time", "guests", "status")
    list_filter = ("date", "status")
    search_fields = ("name", "email")


@admin.register(RestaurantTable)
class RestaurantTableAdmin(admin.ModelAdmin):
    list_display = ("table_number", "seats", "is_active")
    list_filter = ("seats", "is_active")


@admin.register(NewsletterSignup)
class NewsletterSignupAdmin(admin.ModelAdmin):
    list_display = ("email", "created_at", "status")
    list_filter = ("status",)
    search_fields = ("email",)


@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "price", "is_chefs_pick")
    list_filter = ("category", "is_chefs_pick")
    search_fields = ("name", "description")
