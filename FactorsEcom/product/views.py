from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from django.http import HttpResponse
from django.core.paginator import Paginator
from category.models import Category
from .models import Product
from cart.models import CartItems
from cart.views import _cart_id


def store(request, category_slug=None):
    category = None

    products = Product.objects.filter(is_available=True)

    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(product_category=category)

    products = products.order_by('id')  

    paginator = Paginator(products, 3)  
    page = request.GET.get('page')
    paged_products = paginator.get_page(page)

    context = {
        'products': paged_products,
        'product_count': products.count(),
        'category': category,
    }
    return render(request, 'store/store.html', context)


def product_detail(request, category_slug, product_slug):
    single_product = get_object_or_404(
        Product,
        product_category__slug=category_slug,
        product_slug=product_slug,
        is_available=True
    )

    in_cart = CartItems.objects.filter(
        cart__cart_id=_cart_id(request),
        product=single_product
    ).exists()

    context = {
        'single_product': single_product,
        'in_cart': in_cart,
    }
    return render(request, 'store/product_detail.html', context)


def search(request):
    keyword = request.GET.get('keyword', '').strip()

    products = Product.objects.none()
    product_count = 0

    if keyword:
        products = (
            Product.objects
            .filter(
                Q(product_name__icontains=keyword) |
                Q(product_description__icontains=keyword)
            )
            .order_by('-created_at')
        )
        product_count = products.count()

    context = {
        'products': products,
        'product_count': product_count,
        'keyword': keyword,
    }
    return render(request, 'store/store.html', context)
