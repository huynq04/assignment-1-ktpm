import requests
from django.shortcuts import render, redirect
from django.contrib import messages

# Service URLs
CUSTOMER_SERVICE = 'http://localhost:8002/api/customers'
BOOK_SERVICE = 'http://localhost:8003/api/books'
CART_SERVICE = 'http://localhost:8004/api/carts'


def home(request):
    return render(request, 'home.html')


def register(request):
    if request.method == 'POST':
        data = {
            'name': request.POST['name'],
            'email': request.POST['email'],
            'password': request.POST['password']
        }
        try:
            response = requests.post(f'{CUSTOMER_SERVICE}/register/', json=data)
            if response.status_code == 201:
                messages.success(request, 'Đăng ký thành công! Vui lòng đăng nhập.')
                return redirect('login')
            else:
                messages.error(request, 'Đăng ký thất bại!')
        except Exception as e:
            messages.error(request, f'Lỗi kết nối: {str(e)}')
    
    return render(request, 'register.html')


def login_view(request):
    if request.method == 'POST':
        data = {
            'email': request.POST['email'],
            'password': request.POST['password']
        }
        try:
            response = requests.post(f'{CUSTOMER_SERVICE}/login/', json=data)
            if response.status_code == 200:
                user_data = response.json()
                request.session['user_id'] = user_data['id']
                request.session['user_name'] = user_data['name']
                request.session['user_email'] = user_data['email']
                messages.success(request, f'Chào mừng {user_data["name"]}!')
                return redirect('books')
            else:
                messages.error(request, 'Email hoặc mật khẩu không đúng!')
        except Exception as e:
            messages.error(request, f'Lỗi kết nối: {str(e)}')
    
    return render(request, 'login.html')


def logout_view(request):
    request.session.flush()
    messages.success(request, 'Đã đăng xuất!')
    return redirect('home')


def books(request):
    if 'user_id' not in request.session:
        messages.warning(request, 'Vui lòng đăng nhập!')
        return redirect('login')
    
    try:
        response = requests.get(f'{BOOK_SERVICE}/')
        books_list = response.json() if response.status_code == 200 else []
    except Exception as e:
        books_list = []
        messages.error(request, f'Không thể tải danh sách sách: {str(e)}')
    
    return render(request, 'books.html', {'books': books_list})


def add_to_cart(request, book_id):
    if 'user_id' not in request.session:
        return redirect('login')
    
    customer_id = request.session['user_id']
    data = {
        'book_id': book_id,
        'quantity': int(request.POST.get('quantity', 1))
    }
    
    try:
        response = requests.post(f'{CART_SERVICE}/{customer_id}/', json=data)
        if response.status_code == 201:
            messages.success(request, 'Đã thêm sách vào giỏ hàng!')
        else:
            messages.error(request, 'Không thể thêm vào giỏ hàng!')
    except Exception as e:
        messages.error(request, f'Lỗi: {str(e)}')
    
    return redirect('books')


def cart_view(request):
    if 'user_id' not in request.session:
        return redirect('login')
    
    customer_id = request.session['user_id']
    cart_items = []
    total_price = 0
    
    try:
        # Get cart from cart service
        cart_response = requests.get(f'{CART_SERVICE}/{customer_id}/')
        if cart_response.status_code == 200:
            cart_data = cart_response.json()
            
            # Get book details for each cart item
            for item in cart_data.get('items', []):
                book_response = requests.get(f'{BOOK_SERVICE}/{item["book_id"]}/')
                if book_response.status_code == 200:
                    book = book_response.json()
                    item_total = float(book['price']) * item['quantity']
                    cart_items.append({
                        'id': item['id'],
                        'book': book,
                        'quantity': item['quantity'],
                        'total': item_total
                    })
                    total_price += item_total
    except Exception as e:
        messages.error(request, f'Lỗi khi tải giỏ hàng: {str(e)}')
    
    return render(request, 'cart.html', {
        'cart_items': cart_items,
        'total_price': total_price
    })


def remove_from_cart(request, item_id):
    if request.method == 'POST':
        try:
            response = requests.delete(f'{CART_SERVICE}/items/{item_id}/')
            if response.status_code == 200:
                messages.success(request, 'Đã xóa sách khỏi giỏ hàng!')
            else:
                messages.error(request, 'Không thể xóa!')
        except Exception as e:
            messages.error(request, f'Lỗi: {str(e)}')
    
    return redirect('cart')


def update_cart_item(request, item_id):
    if request.method == 'POST':
        quantity = request.POST.get('quantity')
        data = {'quantity': int(quantity)}
        try:
            response = requests.put(f'{CART_SERVICE}/items/{item_id}/update/', json=data)
            if response.status_code == 200:
                messages.success(request, 'Đã cập nhật số lượng!')
            else:
                messages.error(request, 'Không thể cập nhật!')
        except Exception as e:
            messages.error(request, f'Lỗi: {str(e)}')
    
    return redirect('cart')

