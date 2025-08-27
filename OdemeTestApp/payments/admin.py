from django.contrib import admin
from .models import Product, PaymentMethod, Order, PaymentLog

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('name', 'description')

@admin.register(PaymentMethod)
class PaymentMethodAdmin(admin.ModelAdmin):
    list_display = ('display_name', 'name', 'is_active', 'test_mode')
    list_filter = ('is_active', 'test_mode')
    list_editable = ('is_active', 'test_mode')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_id', 'product', 'payment_method', 'amount', 'status', 'created_at')
    list_filter = ('status', 'payment_method', 'created_at')
    search_fields = ('order_id', 'product__name')
    readonly_fields = ('order_id', 'created_at', 'updated_at')

@admin.register(PaymentLog)
class PaymentLogAdmin(admin.ModelAdmin):
    list_display = ('order', 'payment_method', 'status', 'created_at')
    list_filter = ('payment_method', 'status', 'created_at')
    readonly_fields = ('order', 'payment_method', 'request_data', 'response_data', 'status', 'created_at')
