"""
Gerçek Ödeme Sistemleri için Güncellenmiş Views
Bu dosya gerçek ödeme API'larını kullanarak ödeme işlemlerini gerçekleştirir.
"""

from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.conf import settings
import json
import uuid
from .models import Product, PaymentMethod, Order, PaymentLog
from .payment_processors import (
    StripePaymentProcessor, 
    PayPalPaymentProcessor,
    IyzicoPaymentProcessor,
    PaparaPaymentProcessor,
    SquarePaymentProcessor,
    RazorpayPaymentProcessor
)

def payment_page(request, product_id, payment_method_name):
    """Gerçek ödeme sayfası"""
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
    
    # Stripe için özel ayarlar
    if payment_method_name == 'stripe':
        processor = StripePaymentProcessor()
        intent_result = processor.create_payment_intent(order)
        if intent_result['success']:
            context['client_secret'] = intent_result['client_secret']
            context['stripe_publishable_key'] = getattr(settings, 'STRIPE_PUBLISHABLE_KEY', '')
    
    # PayPal için özel ayarlar
    elif payment_method_name == 'paypal':
        context['paypal_client_id'] = getattr(settings, 'PAYPAL_CLIENT_ID', '')
    
    return render(request, f'payments/{payment_method_name}_payment.html', context)

@csrf_exempt
@require_http_methods(["POST"])
def process_stripe_payment(request):
    """Stripe ödeme işlemi"""
    try:
        data = json.loads(request.body)
        order_id = data.get('order_id')
        payment_intent_id = data.get('payment_intent_id')
        
        order = get_object_or_404(Order, order_id=order_id)
        processor = StripePaymentProcessor()
        
        # Ödeme durumunu kontrol et
        result = processor.confirm_payment(payment_intent_id)
        
        # Log kaydet
        PaymentLog.objects.create(
            order=order,
            payment_method='stripe',
            request_data=data,
            response_data=result,
            status='success' if result.get('success') else 'failed'
        )
        
        if result.get('success'):
            order.status = 'paid'
            order.payment_id = result.get('payment_id', '')
            order.save()
            
            return JsonResponse({
                'success': True,
                'message': 'Ödeme başarılı',
                'redirect_url': f'/success/{order.order_id}/'
            })
        else:
            return JsonResponse({
                'success': False,
                'message': result.get('error', 'Ödeme başarısız')
            })
            
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Hata oluştu: {str(e)}'
        })

@csrf_exempt
@require_http_methods(["POST"])
def process_iyzico_payment(request):
    """İyzico ödeme işlemi"""
    try:
        data = json.loads(request.body)
        order_id = data.get('order_id')
        
        order = get_object_or_404(Order, order_id=order_id)
        processor = IyzicoPaymentProcessor()
        
        # Kart bilgileri
        card_data = {
            'cardholder': data.get('cardholder'),
            'card_number': data.get('card_number').replace(' ', ''),
            'expire_month': data.get('expiry')[:2],
            'expire_year': '20' + data.get('expiry')[3:5],
            'cvv': data.get('cvv')
        }
        
        # Alıcı bilgileri
        buyer_data = {
            'id': 'BY789',
            'name': data.get('cardholder', 'Test').split()[0],
            'surname': data.get('cardholder', 'User').split()[-1],
            'phone': '+905350000000',
            'email': 'test@test.com',
            'identity': data.get('identity', '11111111111')
        }
        
        result = processor.create_payment(order, card_data, buyer_data)
        
        # Log kaydet
        PaymentLog.objects.create(
            order=order,
            payment_method='iyzico',
            request_data=data,
            response_data=result,
            status='success' if result.get('success') else 'failed'
        )
        
        if result.get('success'):
            order.status = 'paid'
            order.payment_id = result.get('payment_id', '')
            order.save()
            
            return JsonResponse({
                'success': True,
                'message': 'İyzico ile ödeme başarılı',
                'redirect_url': f'/success/{order.order_id}/'
            })
        else:
            return JsonResponse({
                'success': False,
                'message': result.get('error', 'İyzico ödeme başarısız')
            })
            
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Hata oluştu: {str(e)}'
        })

@csrf_exempt
@require_http_methods(["POST"])
def paypal_create_payment(request):
    """PayPal ödeme oluştur"""
    try:
        data = json.loads(request.body)
        order_id = data.get('order_id')
        
        order = get_object_or_404(Order, order_id=order_id)
        processor = PayPalPaymentProcessor()
        
        return_url = request.build_absolute_uri(f'/paypal/execute/{order.order_id}/')
        cancel_url = request.build_absolute_uri(f'/failed/{order.order_id}/')
        
        result = processor.create_payment(order, return_url, cancel_url)
        
        if result.get('success'):
            return JsonResponse({
                'success': True,
                'approval_url': result['approval_url'],
                'payment_id': result['payment_id']
            })
        else:
            return JsonResponse({
                'success': False,
                'message': result.get('error', 'PayPal ödeme oluşturulamadı')
            })
            
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Hata oluştu: {str(e)}'
        })

def razorpay_payment_page(request, product_id):
    """Razorpay ödeme sayfası"""
    product = get_object_or_404(Product, id=product_id)
    payment_method = get_object_or_404(PaymentMethod, name='razorpay')
    
    # Sipariş oluştur
    order_id = f"ORDER_{uuid.uuid4().hex[:10].upper()}"
    order = Order.objects.create(
        product=product,
        payment_method=payment_method,
        amount=product.price,
        order_id=order_id
    )
    
    processor = RazorpayPaymentProcessor()
    razorpay_order = processor.create_order(order)
    
    context = {
        'product': product,
        'order': order,
        'razorpay_order_id': razorpay_order.get('order_id'),
        'razorpay_key_id': getattr(settings, 'RAZORPAY_KEY_ID', ''),
        'amount': razorpay_order.get('amount'),
        'currency': razorpay_order.get('currency')
    }
    
    return render(request, 'payments/razorpay_payment.html', context)

# Webhook handlers
@csrf_exempt
def stripe_webhook(request):
    """Stripe webhook handler"""
    import stripe
    
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
    endpoint_secret = getattr(settings, 'STRIPE_WEBHOOK_SECRET', '')
    
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError:
        return JsonResponse({'error': 'Invalid payload'}, status=400)
    except stripe.error.SignatureVerificationError:
        return JsonResponse({'error': 'Invalid signature'}, status=400)
    
    # Handle the event
    if event['type'] == 'payment_intent.succeeded':
        payment_intent = event['data']['object']
        order_id = payment_intent['metadata'].get('order_id')
        
        try:
            order = Order.objects.get(order_id=order_id)
            order.status = 'paid'
            order.payment_id = payment_intent['id']
            order.save()
        except Order.DoesNotExist:
            pass
    
    return JsonResponse({'status': 'success'})

@csrf_exempt
def iyzico_webhook(request):
    """İyzico webhook handler"""
    # İyzico webhook implementasyonu
    return JsonResponse({'status': 'success'})

# Utility functions
def get_payment_processor(payment_method_name):
    """Ödeme metoduna göre processor döner"""
    processors = {
        'stripe': StripePaymentProcessor,
        'paypal': PayPalPaymentProcessor,
        'iyzico': IyzicoPaymentProcessor,
        'papara': PaparaPaymentProcessor,
        'square': SquarePaymentProcessor,
        'razorpay': RazorpayPaymentProcessor,
    }
    
    processor_class = processors.get(payment_method_name)
    if processor_class:
        return processor_class()
    return None

def validate_payment_data(payment_method, data):
    """Ödeme verilerini doğrular"""
    required_fields = {
        'stripe': ['payment_intent_id'],
        'paypal': ['payment_id', 'payer_id'],
        'iyzico': ['card_number', 'expiry', 'cvv', 'cardholder'],
        'papara': ['papara_number', 'password'],
        'square': ['source_id'],
        'razorpay': ['razorpay_payment_id', 'razorpay_signature']
    }
    
    required = required_fields.get(payment_method, [])
    missing = [field for field in required if not data.get(field)]
    
    return len(missing) == 0, missing
