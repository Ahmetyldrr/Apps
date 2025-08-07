from django.urls import path
from . import views
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('detail/', views.detail, name='detail'),
    path('contact/', views.contact, name='contact'),
    path('products/', views.products, name='products'),
    path('addData/', views.addData, name='addData'),
]