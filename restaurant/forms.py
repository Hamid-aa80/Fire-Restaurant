from decimal import Decimal

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.utils import timezone

from .models import Reservation, RestaurantTable


class CustomerRegistrationForm(UserCreationForm):
    name = forms.CharField(max_length=150, widget=forms.TextInput(attrs={"class": "form-control"}))
    email = forms.EmailField(
        max_length=150,
        label="Email address",
        widget=forms.EmailInput(attrs={"class": "form-control"}),
    )

    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ("email",)

    def clean_email(self):
        email = self.cleaned_data["email"].strip().lower()
        if get_user_model().objects.filter(username__iexact=email).exists():
            raise forms.ValidationError("An account with this email already exists.")
        return email

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["password1"].widget.attrs["class"] = "form-control"
        self.fields["password2"].widget.attrs["class"] = "form-control"

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data["email"]
        user.email = self.cleaned_data["email"]
        user.first_name = self.cleaned_data["name"].strip()
        if commit:
            user.save()
        return user


class CustomerLoginForm(forms.Form):
    email = forms.EmailField(
        max_length=150,
        widget=forms.EmailInput(attrs={"class": "form-control"}),
    )
    password = forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-control"}))


class ReservationForm(forms.Form):
    date = forms.DateField(
        input_formats=["%Y-%m-%d"],
        widget=forms.DateInput(attrs={"class": "form-control", "type": "date"}),
    )
    time = forms.TimeField(
        input_formats=["%H:%M", "%H:%M:%S"],
        widget=forms.TimeInput(attrs={"class": "form-control", "type": "time"}),
    )
    guests = forms.IntegerField(
        min_value=1,
        max_value=4,
        widget=forms.NumberInput(attrs={"class": "form-control", "min": 1, "max": 4}),
    )
    requests = forms.CharField(
        required=False,
        max_length=2000,
        widget=forms.Textarea(attrs={"class": "form-control", "rows": 3}),
    )
    table = forms.ModelChoiceField(queryset=RestaurantTable.objects.none())

    def __init__(self, *args, customer=None, reservation=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.customer = customer
        self.reservation = reservation
        self.fields["table"].queryset = RestaurantTable.objects.filter(is_active=True)

    def clean_date(self):
        reservation_date = self.cleaned_data["date"]
        if reservation_date < timezone.localdate():
            raise forms.ValidationError("Reservations cannot be made for past dates.")
        return reservation_date

    def clean(self):
        cleaned_data = super().clean()
        reservation_date = cleaned_data.get("date")
        reservation_time = cleaned_data.get("time")
        guests = cleaned_data.get("guests")
        table = cleaned_data.get("table")

        if reservation_date == timezone.localdate() and reservation_time:
            if reservation_time <= timezone.localtime().time().replace(second=0, microsecond=0):
                self.add_error("time", "Reservations cannot be made for past times.")

        if table and guests and table.seats < guests:
            self.add_error("table", "The selected table does not have enough seats.")

        if reservation_date and reservation_time and table:
            conflicts = Reservation.objects.filter(date=reservation_date, time=reservation_time)
            if self.reservation:
                conflicts = conflicts.exclude(pk=self.reservation.pk)
            if conflicts.filter(table=table).exists():
                self.add_error("table", "That table is already booked at this date and time.")
            if self.customer and conflicts.filter(customer=self.customer).exists():
                self.add_error(None, "You already have a reservation at this date and time.")
        return cleaned_data


class ReservationAvailabilityForm(forms.Form):
    date = forms.DateField(input_formats=["%Y-%m-%d"])
    time = forms.TimeField(input_formats=["%H:%M", "%H:%M:%S"])
    guests = forms.IntegerField(min_value=1, max_value=4)

    def clean_date(self):
        reservation_date = self.cleaned_data["date"]
        if reservation_date < timezone.localdate():
            raise forms.ValidationError("Choose today or a future date.")
        return reservation_date

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get("date") == timezone.localdate() and cleaned_data.get("time"):
            if cleaned_data["time"] <= timezone.localtime().time().replace(second=0, microsecond=0):
                self.add_error("time", "Choose a future time.")
        return cleaned_data


class NewsletterSignupForm(forms.Form):
    email = forms.EmailField(max_length=254)


class MenuItemForm(forms.Form):
    name = forms.CharField(min_length=1, max_length=150)
    category = forms.CharField(min_length=1, max_length=100)
    description = forms.CharField(required=False, max_length=2000)
    price = forms.DecimalField(required=False, min_value=0, max_digits=8, decimal_places=2)
    image = forms.CharField(required=False, max_length=500)
    is_chefs_pick = forms.BooleanField(required=False)

    def clean_price(self):
        return self.cleaned_data.get("price") or Decimal("0.00")
