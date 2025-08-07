from django.shortcuts import render, get_object_or_404, redirect
from .models import Product
from django.db import transaction

def product_list(request):
    products = Product.objects.all()
    return render(request, 'store/product_list.html', {'products': products})

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'store/product_detail.html', {'product': product})

def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = request.session.get('cart', {})
    
    cart_item = cart.get(str(product_id), {'quantity': 0})
    cart_item['quantity'] += 1
    cart[str(product_id)] = cart_item
    
    request.session['cart'] = cart
    return redirect('cart_detail')

def remove_from_cart(request, product_id):
    cart = request.session.get('cart', {})
    if str(product_id) in cart:
        del cart[str(product_id)]
        request.session['cart'] = cart
    return redirect('cart_detail')

def cart_detail(request):
    cart = request.session.get('cart', {})
    cart_items = []
    total_price = 0
    
    for product_id, item_data in cart.items():
        product = get_object_or_404(Product, id=int(product_id))
        quantity = item_data['quantity']
        price = product.price * quantity
        total_price += price
        cart_items.append({
            'product': product,
            'quantity': quantity,
            'price': price
        })
        
    return render(request, 'store/cart_detail.html', {
        'cart_items': cart_items,
        'total_price': total_price
    })

@transaction.atomic
def checkout(request):
    cart = request.session.get('cart', {})
    if not cart:
        return redirect('cart_detail')

    # Stokları kontrol et ve düşür
    for product_id, item_data in cart.items():
        product = get_object_or_404(Product, id=int(product_id))
        quantity = item_data['quantity']
        
        if product.stock < quantity:
            # Yetersiz stok durumunda (şimdilik) sepete geri yönlendir
            # Gerçek bir uygulamada kullanıcıya bir hata mesajı gösterilebilir
            return redirect('cart_detail')
        
        product.stock -= quantity
        product.save()

    # Sepeti temizle
    del request.session['cart']
    
    # Başarı sayfasına yönlendir
    return render(request, 'store/checkout_success.html')