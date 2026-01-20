from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Cart, CartItem
from .serializers import CartSerializer, CartItemSerializer
from books.models import Book

class CartViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Cart.objects.filter(customer=self.request.user)
    
    @action(detail=False, methods=['get'])
    def current(self, request):
        """Get or create current user's cart"""
        cart, created = Cart.objects.get_or_create(customer=request.user)
        serializer = self.get_serializer(cart)
        return Response(serializer.data)
    
    @action(detail=False, methods=['post'])
    def add_item(self, request):
        """Add item to cart"""
        book_id = request.data.get('book_id')
        quantity = request.data.get('quantity', 1)
        
        if not book_id:
            return Response(
                {'error': 'book_id is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            book = Book.objects.get(id=book_id)
        except Book.DoesNotExist:
            return Response(
                {'error': 'Book not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        
        if book.stock < quantity:
            return Response(
                {'error': f'Only {book.stock} items available in stock'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        cart, _ = Cart.objects.get_or_create(customer=request.user)
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart, 
            book=book,
            defaults={'quantity': quantity}
        )
        
        if not created:
            cart_item.quantity += quantity
            cart_item.save()
        
        serializer = CartItemSerializer(cart_item)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    @action(detail=False, methods=['delete'])
    def clear(self, request):
        """Clear all items from cart"""
        try:
            cart = Cart.objects.get(customer=request.user)
            cart.cartitem_set.all().delete()
            return Response(
                {'message': 'Cart cleared successfully'}, 
                status=status.HTTP_204_NO_CONTENT
            )
        except Cart.DoesNotExist:
            return Response(
                {'message': 'Cart is already empty'}, 
                status=status.HTTP_200_OK
            )

class CartItemViewSet(viewsets.ModelViewSet):
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return CartItem.objects.filter(cart__customer=self.request.user)
    
    def perform_create(self, serializer):
        cart, _ = Cart.objects.get_or_create(customer=self.request.user)
        serializer.save(cart=cart)
    
    def update(self, request, *args, **kwargs):
        """Update cart item quantity"""
        instance = self.get_object()
        quantity = request.data.get('quantity')
        
        if quantity is not None:
            if quantity < 1:
                return Response(
                    {'error': 'Quantity must be at least 1'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            if instance.book.stock < quantity:
                return Response(
                    {'error': f'Only {instance.book.stock} items available'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
        
        return super().update(request, *args, **kwargs)
