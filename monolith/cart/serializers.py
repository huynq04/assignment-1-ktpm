from rest_framework import serializers
from .models import Cart, CartItem
from books.serializers import BookSerializer

class CartItemSerializer(serializers.ModelSerializer):
    book = BookSerializer(read_only=True)
    book_id = serializers.IntegerField(write_only=True)
    subtotal = serializers.SerializerMethodField()
    
    class Meta:
        model = CartItem
        fields = ['id', 'cart', 'book', 'book_id', 'quantity', 'subtotal']
        read_only_fields = ['id', 'cart']
    
    def get_subtotal(self, obj):
        return obj.book.price * obj.quantity
    
    def validate_quantity(self, value):
        if value < 1:
            raise serializers.ValidationError("Quantity must be at least 1")
        return value

class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True, source='cartitem_set')
    total_items = serializers.SerializerMethodField()
    total_price = serializers.SerializerMethodField()
    
    class Meta:
        model = Cart
        fields = ['id', 'customer', 'created_at', 'items', 'total_items', 'total_price']
        read_only_fields = ['id', 'customer', 'created_at']
    
    def get_total_items(self, obj):
        return sum(item.quantity for item in obj.cartitem_set.all())
    
    def get_total_price(self, obj):
        return sum(item.book.price * item.quantity for item in obj.cartitem_set.all())
