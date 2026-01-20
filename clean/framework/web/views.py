from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required

# Import use cases
from usecases.customer_usecases import (
    RegisterCustomerUseCase,
    LoginCustomerUseCase,
    AddToCartUseCase,
    ViewCartUseCase,
    RemoveFromCartUseCase,
    UpdateCartItemQuantityUseCase
)
from usecases.book_usecases import ListBooksUseCase

# Import repositories
from infrastructure.django_repositories import (
    DjangoCustomerRepository,
    DjangoBookRepository,
    DjangoCartRepository,
    DjangoCartItemRepository
)

# Initialize repositories
customer_repo = DjangoCustomerRepository()
book_repo = DjangoBookRepository()
cart_repo = DjangoCartRepository()
cart_item_repo = DjangoCartItemRepository()

# Initialize use cases
register_usecase = RegisterCustomerUseCase(customer_repo)
login_usecase = LoginCustomerUseCase(customer_repo)
list_books_usecase = ListBooksUseCase(book_repo)
add_to_cart_usecase = AddToCartUseCase(cart_repo, cart_item_repo, book_repo)
view_cart_usecase = ViewCartUseCase(cart_repo, cart_item_repo, book_repo)
remove_from_cart_usecase = RemoveFromCartUseCase(cart_item_repo)
update_cart_item_usecase = UpdateCartItemQuantityUseCase(cart_item_repo, book_repo)


def home(request):
    """Home page"""
    return render(request, 'home.html')


def register(request):
    """Customer registration"""
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        name = request.POST.get('name')
        
        try:
            customer = register_usecase.execute(name, email, password)
            messages.success(request, 'Đăng ký thành công! Vui lòng đăng nhập.')
            return redirect('login')
        except ValueError as e:
            messages.error(request, str(e))
    
    return render(request, 'register.html')


def login_view(request):
    """Customer login"""
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        customer = login_usecase.execute(email, password)
        if customer:
            # Get CustomerModel instance from database
            from .models import CustomerModel
            user = CustomerModel.objects.get(id=customer.id)
            auth_login(request, user)
            messages.success(request, f'Chào mừng {customer.name}!')
            return redirect('books')
        else:
            messages.error(request, 'Email hoặc mật khẩu không đúng!')
    
    return render(request, 'login.html')


@login_required
def logout_view(request):
    """Customer logout"""
    auth_logout(request)
    messages.success(request, 'Đăng xuất thành công!')
    return redirect('home')


@login_required
def books(request):
    """List all books"""
    books = list_books_usecase.execute()
    return render(request, 'books.html', {'books': books})


@login_required
def add_to_cart_view(request, book_id):
    """Add book to cart"""
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        
        try:
            add_to_cart_usecase.execute(request.user.id, book_id, quantity)
            messages.success(request, 'Đã thêm sách vào giỏ hàng!')
        except ValueError as e:
            messages.error(request, str(e))
    
    return redirect('books')


@login_required
def cart_view(request):
    """View cart"""
    cart_data = view_cart_usecase.execute(request.user.id)
    
    cart_items = []
    for item_data in cart_data['items']:
        cart_items.append({
            'id': item_data['item'].id,
            'book': item_data['book'],
            'quantity': item_data['item'].quantity,
            'total': item_data['subtotal']
        })
    
    return render(request, 'cart.html', {
        'cart_items': cart_items,
        'total_price': cart_data['total']
    })


@login_required
def remove_from_cart_view(request, item_id):
    """Remove item from cart"""
    try:
        remove_from_cart_usecase.execute(item_id)
        messages.success(request, 'Đã xóa sách khỏi giỏ hàng!')
    except ValueError as e:
        messages.error(request, str(e))
    
    return redirect('cart')


@login_required
def update_cart_item_view(request, item_id):
    """Update cart item quantity"""
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        
        try:
            update_cart_item_usecase.execute(item_id, quantity)
            messages.success(request, 'Đã cập nhật số lượng!')
        except ValueError as e:
            messages.error(request, str(e))
    
    return redirect('cart')

