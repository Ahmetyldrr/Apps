from django.db import models
from django.contrib.auth.models import User

class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image_url = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name

class PaymentMethod(models.Model):
    PAYMENT_CHOICES = [
        ('stripe', 'Stripe'),
        ('paypal', 'PayPal'),
        ('square', 'Square'),
        ('razorpay', 'Razorpay'),
        ('iyzico', 'Iyzico'),
        ('papara', 'Papara'),
    ]
    
    name = models.CharField(max_length=20, choices=PAYMENT_CHOICES, unique=True)
    display_name = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)
    test_mode = models.BooleanField(default=True)
    api_key = models.CharField(max_length=200, blank=True)
    secret_key = models.CharField(max_length=200, blank=True)
    
    def __str__(self):
        return self.display_name

class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Bekliyor'),
        ('paid', 'Ödendi'),
        ('failed', 'Başarısız'),
        ('cancelled', 'İptal Edildi'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    payment_method = models.ForeignKey(PaymentMethod, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    order_id = models.CharField(max_length=100, unique=True)
    payment_id = models.CharField(max_length=200, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Order {self.order_id} - {self.product.name}"

class PaymentLog(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    payment_method = models.CharField(max_length=20)
    request_data = models.JSONField()
    response_data = models.JSONField()
    status = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Payment Log - {self.order.order_id}"
