from django.contrib import admin
from .models import Product


class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {'product_slug':('product_name',)}
    list_display = ('product_name','product_slug', 'product_price','is_available','created_at','updated_at')
    search_fields = ('product_name',)

admin.site.register(Product, ProductAdmin)
