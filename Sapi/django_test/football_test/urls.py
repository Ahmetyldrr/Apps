"""football_test URL Configuration"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('football.urls')),
]

# Admin site customization
admin.site.site_header = "⚽ Futbol Veri Yönetimi"
admin.site.site_title = "Football Admin"
admin.site.index_title = "Futbol Veritabanı Yönetimi"
