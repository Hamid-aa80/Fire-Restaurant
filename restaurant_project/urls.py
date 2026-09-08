from django.contrib import admin
from django.urls import include, path

from restaurant_app.views import account_page

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('restaurant_app.urls')),
    path('account/', account_page, name='account'),
]
