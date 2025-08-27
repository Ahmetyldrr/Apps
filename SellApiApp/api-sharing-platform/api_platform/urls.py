from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from rest_framework.routers import DefaultRouter
from apps.accounts.views import HomeView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', HomeView.as_view(), name='home'),
    path('accounts/', include('apps.accounts.urls')),
    path('apis/', include('apps.apis.urls')),
    path('api/', include('rest_framework.urls')),  # DRF login/logout views
]