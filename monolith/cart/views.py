from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Cart, CartItem
from books.models import Book

@login_required
def add_to_cart(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    
    if book.stock < 1:
        messages.error(request, f'Sorry, "{book.title}" is out of stock.')
        return redirect('book_list')
    
    cart, _ = Cart.objects.get_or_create(customer=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, book=book)
    
    if not created:
        if book.stock < cart_item.quantity + 1:
            messages.warning(request, f'Only {book.stock} copies of "{book.title}" available.')
            return redirect('book_list')
        cart_item.quantity += 1
        cart_item.save()
        messages.success(request, f'Added another copy of "{book.title}" to your cart.')
    else:
        messages.success(request, f'"{book.title}" added to your cart!')
    
    return redirect('view_cart')

@login_required
def view_cart(request):
    try:
        cart = Cart.objects.get(customer=request.user)
        cart_items_qs = CartItem.objects.filter(cart=cart).select_related('book')
        
        # Format data to match template expectations
        cart_items = []
        total_price = 0
        for cart_item in cart_items_qs:
            item_total = cart_item.book.price * cart_item.quantity
            cart_items.append({
                'id': cart_item.id,
                'book': cart_item.book,
                'quantity': cart_item.quantity,
                'total': item_total
            })
            total_price += item_total
    except Cart.DoesNotExist:
        cart_items = []
        total_price = 0
    
    return render(request, 'cart/cart.html', {
        'cart_items': cart_items,
        'total_price': total_price
    })

@login_required
def remove_from_cart(request, item_id):
    """Remove item from cart"""
    if request.method == 'POST':
        cart_item = get_object_or_404(CartItem, id=item_id)
        if cart_item.cart.customer == request.user:
            book_title = cart_item.book.title
            cart_item.delete()
            messages.success(request, f'Đã xóa "{book_title}" khỏi giỏ hàng!')
        else:
            messages.error(request, 'Không thể xóa sản phẩm này.')
    return redirect('view_cart')

@login_required
def update_cart_item(request, item_id):
    """Update cart item quantity"""
    if request.method == 'POST':
        cart_item = get_object_or_404(CartItem, id=item_id)
        if cart_item.cart.customer == request.user:
            quantity = int(request.POST.get('quantity', 1))
            if quantity > 0:
                if quantity <= cart_item.book.stock:
                    cart_item.quantity = quantity
                    cart_item.save()
                    messages.success(request, f'Đã cập nhật số lượng!')
                else:
                    messages.error(request, f'Chỉ còn {cart_item.book.stock} quyển.')
            else:
                messages.error(request, 'Số lượng phải lớn hơn 0.')
        else:
            messages.error(request, 'Không thể cập nhật sản phẩm này.')
    return redirect('view_cart')