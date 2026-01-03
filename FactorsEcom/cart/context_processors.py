from .models import Cart, CartItems
from .views import _cart_id


def counter(request):
    cart_count = 0

    if 'admin' in request.path:
        return {}

    cart = Cart.objects.filter(cart_id=_cart_id(request)).first()

    if cart:
        cart_items = CartItems.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items:
            cart_count += cart_item.quantity

    return dict(cart_count=cart_count)
