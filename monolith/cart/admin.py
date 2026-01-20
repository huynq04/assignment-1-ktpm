from django.contrib import admin
from .models import Cart, CartItem

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('customer', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('customer__email', 'customer__name')
    ordering = ('-created_at',)

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('cart', 'book', 'quantity')
    list_filter = ('cart__created_at',)
    search_fields = ('cart__customer__email', 'book__title')
    ordering = ('-cart__created_at',)
