from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Cart, CartItem
from .serializers import CartSerializer, CartItemSerializer


@api_view(['GET', 'POST'])
def cart_view(request, customer_id):
    if request.method == 'GET':
        try:
            cart = Cart.objects.get(customer_id=customer_id)
            serializer = CartSerializer(cart)
            return Response(serializer.data)
        except Cart.DoesNotExist:
            return Response({'items': []}, status=status.HTTP_200_OK)
    
    elif request.method == 'POST':
        cart, created = Cart.objects.get_or_create(customer_id=customer_id)
        book_id = request.data.get('book_id')
        quantity = request.data.get('quantity', 1)
        
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            book_id=book_id,
            defaults={'quantity': quantity}
        )
        
        if not created:
            cart_item.quantity += quantity
            cart_item.save()
        
        serializer = CartSerializer(cart)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['DELETE'])
def remove_item(request, item_id):
    try:
        cart_item = CartItem.objects.get(id=item_id)
        cart_item.delete()
        return Response({'message': 'Item removed'}, status=status.HTTP_200_OK)
    except CartItem.DoesNotExist:
        return Response({'error': 'Item not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['PUT'])
def update_item(request, item_id):
    try:
        cart_item = CartItem.objects.get(id=item_id)
        quantity = request.data.get('quantity')
        if quantity:
            cart_item.quantity = quantity
            cart_item.save()
        serializer = CartItemSerializer(cart_item)
        return Response(serializer.data)
    except CartItem.DoesNotExist:
        return Response({'error': 'Item not found'}, status=status.HTTP_404_NOT_FOUND)

