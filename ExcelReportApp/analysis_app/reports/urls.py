from django.urls import path
from . import views

urlpatterns = [
    path('', views.analysis_list, name='analysis_list'),
    path('download/<int:pk>/', views.download_analysis, name='download_analysis'),
]
