from django.contrib import admin
from .models import CustomerModel, BookModel, CartModel, CartItemModel

@admin.register(CustomerModel)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['id', 'email', 'name', 'is_active', 'date_joined']
    search_fields = ['email', 'name']
    list_filter = ['is_active', 'date_joined']

@admin.register(BookModel)
class BookAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'author', 'price', 'stock']
    search_fields = ['title', 'author']
    list_filter = ['author']

@admin.register(CartModel)
class CartAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer', 'created_at']
    search_fields = ['customer__email']

@admin.register(CartItemModel)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'cart', 'book', 'quantity']
    search_fields = ['book__title']

