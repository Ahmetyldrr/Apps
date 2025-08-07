from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('upload/', views.upload_excel, name='upload_excel'),
    path('analysis/', views.data_analysis, name='data_analysis'),
    path('energy-analysis/', views.energy_analysis, name='energy_analysis'),
    path('smf-prediction/', views.smf_direction_prediction, name='smf_prediction'),
    path('models/', views.forecast_models, name='forecast_models'),
    path('ai-analysis/', views.ai_analysis_view, name='ai_analysis'),
    path('api/forecast/', views.api_forecast, name='api_forecast'),
    path('api/ai-insight/', views.generate_ai_insight, name='generate_ai_insight'),
]
