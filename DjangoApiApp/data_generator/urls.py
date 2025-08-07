from django.urls import path
from .views import GenerateForecastView, ForecastDashboardView, DownloadForecastView

urlpatterns = [
    path('', ForecastDashboardView.as_view(), name='forecast-dashboard'),
    path('generate-forecast/', GenerateForecastView.as_view(), name='generate-forecast'),
    path('download-forecast/', DownloadForecastView.as_view(), name='download-forecast'),
]
