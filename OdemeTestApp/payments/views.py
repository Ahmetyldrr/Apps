from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json
import uuid
import requests
from .models import Product, PaymentMethod, Order, PaymentLog

def home(request):
    """Ana sayfa - Ürünleri listeler"""
    products = Product.objects.all()
    return render(request, 'payments/home.html', {'products': products})

def product_detail(request, product_id):
    """Ürün detay sayfası"""
    product = get_object_or_404(Product, id=product_id)
    payment_methods = PaymentMethod.objects.filter(is_active=True)
    return render(request, 'payments/product_detail.html', {
        'product': product,
        'payment_methods': payment_methods
    })

def payment_page(request, product_id, payment_method_name):
    """Ödeme sayfası"""
    product = get_object_or_404(Product, id=product_id)
    payment_method = get_object_or_404(PaymentMethod, name=payment_method_name)
    
    # Sipariş oluştur
    order_id = f"ORDER_{uuid.uuid4().hex[:10].upper()}"
    order = Order.objects.create(
        product=product,
        payment_method=payment_method,
        amount=product.price,
        order_id=order_id
    )
    
    context = {
        'product': product,
        'payment_method': payment_method,
        'order': order
    }
    
    return render(request, f'payments/{payment_method_name}_payment.html', context)

@csrf_exempt
@require_http_methods(["POST"])
def process_payment(request):
    """Ödeme işlemini gerçekleştirir"""
    try:
        data = json.loads(request.body)
        order_id = data.get('order_id')
        payment_method = data.get('payment_method')
        
        order = get_object_or_404(Order, order_id=order_id)
        
        # Ödeme metoduna göre işlem yap
        if payment_method == 'stripe':
            result = process_stripe_payment(order, data)
        elif payment_method == 'paypal':
            result = process_paypal_payment(order, data)
        elif payment_method == 'square':
            result = process_square_payment(order, data)
        elif payment_method == 'razorpay':
            result = process_razorpay_payment(order, data)
        elif payment_method == 'iyzico':
            result = process_iyzico_payment(order, data)
        elif payment_method == 'papara':
            result = process_papara_payment(order, data)
        else:
            result = {'success': False, 'message': 'Geçersiz ödeme metodu'}
        
        # Log kaydet
        PaymentLog.objects.create(
            order=order,
            payment_method=payment_method,
            request_data=data,
            response_data=result,
            status='success' if result.get('success') else 'failed'
        )
        
        if result.get('success'):
            order.status = 'paid'
            order.payment_id = result.get('payment_id', '')
            order.save()
        
        return JsonResponse(result)
        
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})

def success_page(request, order_id):
    """Başarılı ödeme sayfası"""
    order = get_object_or_404(Order, order_id=order_id)
    return render(request, 'payments/success.html', {'order': order})

def failed_page(request, order_id):
    """Başarısız ödeme sayfası"""
    order = get_object_or_404(Order, order_id=order_id)
    return render(request, 'payments/failed.html', {'order': order})

# Ödeme metodu fonksiyonları (Test amaçlı)
def process_stripe_payment(order, data):
    """Stripe ödeme simülasyonu"""
    # Gerçek uygulamada Stripe API kullanılır
    return {
        'success': True,
        'message': 'Stripe ile ödeme başarılı (Test)',
        'payment_id': f'stripe_{uuid.uuid4().hex[:8]}'
    }

def process_paypal_payment(order, data):
    """PayPal ödeme simülasyonu"""
    # Gerçek uygulamada PayPal API kullanılır
    return {
        'success': True,
        'message': 'PayPal ile ödeme başarılı (Test)',
        'payment_id': f'paypal_{uuid.uuid4().hex[:8]}'
    }

def process_square_payment(order, data):
    """Square ödeme simülasyonu"""
    return {
        'success': True,
        'message': 'Square ile ödeme başarılı (Test)',
        'payment_id': f'square_{uuid.uuid4().hex[:8]}'
    }

def process_razorpay_payment(order, data):
    """Razorpay ödeme simülasyonu"""
    return {
        'success': True,
        'message': 'Razorpay ile ödeme başarılı (Test)',
        'payment_id': f'razorpay_{uuid.uuid4().hex[:8]}'
    }

def process_iyzico_payment(order, data):
    """Iyzico ödeme simülasyonu"""
    return {
        'success': True,
        'message': 'Iyzico ile ödeme başarılı (Test)',
        'payment_id': f'iyzico_{uuid.uuid4().hex[:8]}'
    }

def process_papara_payment(order, data):
    """Papara ödeme simülasyonu"""
    return {
        'success': True,
        'message': 'Papara ile ödeme başarılı (Test)',
        'payment_id': f'papara_{uuid.uuid4().hex[:8]}'
    }
