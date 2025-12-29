from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from .models import Cart, CartItems
from product.models import Product
from django.http import HttpResponse


def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart
    
    
def add_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
    except Cart.DoesNotExist:
        cart = Cart.objects.create(
            cart_id=_cart_id(request)
        )
        cart.save()
    
    try:
        cart_item = CartItems.objects.get(
            product=product,
            cart=cart
        )
        cart_item.quantity += 1
        cart_item.save()
    except CartItems.DoesNotExist:
        cart_item = CartItems.objects.create(
            product=product,
            cart=cart,
            quantity=1
        )
        cart_item.save()
    return redirect('cart')

 
def remove_cart(request, product_id):
    cart = Cart.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(Product, id=product_id) 
    cart_item = CartItems.objects.get(product=product, cart=cart)

    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
        return redirect('home')
    return redirect('cart')

def delete_cart_item(request, product_id):
    cart = Cart.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(Product, id=product_id)

    cart_item = CartItems.objects.get(product=product, cart=cart)

    cart_item.delete()
    return redirect('cart')


def cart(request, total=0, quantity=0, cart_items=None):
    delivery_charge = 110
    grand_total = 0

    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItems.objects.filter(cart=cart, is_active=True)

        for cartitem in cart_items:
            total += cartitem.product.product_price * cartitem.quantity
            quantity += cartitem.quantity

        grand_total = total + delivery_charge if total > 0 else 0

    except ObjectDoesNotExist:
        cart_items = []

    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'grand_total': grand_total,
    }

    return render(request, 'store/cart.html', context)