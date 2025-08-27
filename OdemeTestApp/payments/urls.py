from django.urls import path
from . import views

app_name = 'payments'

urlpatterns = [
    path('', views.home, name='home'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('payment/<int:product_id>/<str:payment_method_name>/', views.payment_page, name='payment_page'),
    path('process-payment/', views.process_payment, name='process_payment'),
    path('success/<str:order_id>/', views.success_page, name='success'),
    path('failed/<str:order_id>/', views.failed_page, name='failed'),
]
