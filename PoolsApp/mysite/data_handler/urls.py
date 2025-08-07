from django.urls import path
from . import views

app_name = 'data_handler'

urlpatterns = [
    # The path is now '' because 'upload/' is handled in the main urls.py
    path('', views.upload_polls, name='upload_polls'),
    
    # Path for downloading the Excel template
    path('download-template/', views.download_template, name='download_template'),
]
