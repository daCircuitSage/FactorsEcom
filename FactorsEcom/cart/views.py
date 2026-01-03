from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from .models import Cart, CartItems
from product.models import Product


DELIVERY_CHARGE = 110


def _cart_id(request):
    cart_id = request.session.session_key
    if not cart_id:
        cart_id = request.session.create()
    return cart_id


def add_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart_id = _cart_id(request)

    cart, _ = Cart.objects.get_or_create(cart_id=cart_id)

    cart_item, created = CartItems.objects.get_or_create(
        product=product,
        cart=cart,
        defaults={'quantity': 1}
    )

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect('cart')


def remove_cart(request, product_id):
    cart = get_object_or_404(Cart, cart_id=_cart_id(request))
    product = get_object_or_404(Product, id=product_id)

    cart_item = get_object_or_404(CartItems, product=product, cart=cart)

    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()

    return redirect('cart')


def delete_cart_item(request, product_id):
    cart = get_object_or_404(Cart, cart_id=_cart_id(request))
    product = get_object_or_404(Product, id=product_id)

    cart_item = get_object_or_404(CartItems, product=product, cart=cart)
    cart_item.delete()

    return redirect('cart')


def cart(request):
    total = 0
    quantity = 0
    cart_items = []
    grand_total = 0

    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItems.objects.filter(cart=cart, is_active=True)

        for item in cart_items:
            total += item.product.product_price * item.quantity
            quantity += item.quantity

        if total > 0:
            grand_total = total + DELIVERY_CHARGE

    except ObjectDoesNotExist:
        pass

    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'delivery_charge': DELIVERY_CHARGE,
        'grand_total': grand_total,
    }

    return render(request, 'store/cart.html', context)
