# Microservices Architecture - BookStore

## Cấu trúc hệ thống
Hệ thống gồm 3 microservices độc lập và 1 Gateway:

### 1. Customer Service (Port 8002)
- **Database**: customer_db
- **Chức năng**: Quản lý tài khoản người dùng
- **APIs**:
  - POST `/api/customers/register/` - Đăng ký
  - POST `/api/customers/login/` - Đăng nhập
  - GET `/api/customers/<id>/` - Thông tin customer
  - GET `/api/customers/` - Danh sách customers

### 2. Book Service (Port 8003)
- **Database**: book_db
- **Chức năng**: Quản lý danh mục sách
- **APIs**:
  - GET `/api/books/` - Danh sách sách
  - GET `/api/books/<id>/` - Chi tiết sách
  - PUT `/api/books/<id>/stock/` - Cập nhật tồn kho

### 3. Cart Service (Port 8004)
- **Database**: cart_db
- **Chức năng**: Quản lý giỏ hàng
- **APIs**:
  - GET `/api/carts/<customer_id>/` - Xem giỏ hàng
  - POST `/api/carts/<customer_id>/` - Thêm vào giỏ
  - DELETE `/api/carts/items/<item_id>/` - Xóa item
  - PUT `/api/carts/items/<item_id>/update/` - Cập nhật số lượng

### 4. Gateway (Port 8005)
- **Chức năng**: Web interface gọi các microservices
- **Công nghệ**: Django + Requests library
- **URL**: http://localhost:8005/

## Thiết lập lần đầu

### 1. Tạo môi trường ảo (Virtual Environment)
```bash
# Di chuyển vào thư mục micro
cd /Users/huynq/Workspace/python/kttkpm/Assignment_01_v3/micro

# Tạo môi trường ảo
python3 -m venv venv

# Kích hoạt môi trường ảo
source venv/bin/activate

# Để thoát môi trường ảo (khi cần)
# deactivate
```

### 2. Cài đặt dependencies
```bash
# Đảm bảo đã kích hoạt virtual environment
pip3 install -r requirements.txt
```

### 3. Cài đặt và khởi động MySQL
```bash
# Cài đặt MySQL qua Homebrew (nếu chưa có)
brew install mysql

# Khởi động MySQL
brew services start mysql

# Hoặc chạy tạm thời
mysql.server start
```

### 4. Tạo databases trong MySQL
```bash
# Đăng nhập vào MySQL
mysql -u root -p

# Trong MySQL shell, chạy các lệnh sau:
```
```sql
CREATE DATABASE customer_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE DATABASE book_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE DATABASE cart_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
exit;
```

### 5. Cấu hình database password
Mở các file settings và thay đổi password MySQL:
- `customer-service/customer_service/settings.py`
- `book-service/book_service/settings.py`
- `cart-service/cart_service/settings.py`

Tìm section `DATABASES` và cập nhật `PASSWORD`:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'xxx_db',
        'USER': 'root',
        'PASSWORD': 'your_mysql_password',  # Thay đổi password MySQL của bạn
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```

### 6. Chạy migrations cho từng service
```bash
# Customer Service
cd customer-service && python3 manage.py migrate && cd ..

# Book Service
cd book-service && python3 manage.py migrate && cd ..

# Cart Service
cd cart-service && python3 manage.py migrate && cd ..

# Gateway
cd gateway && python3 manage.py migrate && cd ..
```

### 7. Tạo dữ liệu mẫu

#### a. Tạo superuser cho Customer Service
```bash
cd customer-service
python3 manage.py shell
```
Trong shell:
```python
from customers.models import Customer
from django.contrib.auth.hashers import make_password

admin = Customer.objects.create(
    name='Admin',
    email='admin@bookstore.com',
    password=make_password('admin123'),
    is_staff=True,
    is_superuser=True
)
print(f'Created superuser: {admin.email}')
exit()
```

#### b. Tạo superuser cho Book Service
```bash
cd book-service
python3 manage.py createsuperuser --username admin --email admin@bookstore.com
# Password: admin123
cd ..
```

#### c. Tạo superuser cho Cart Service
```bash
cd cart-service
python3 manage.py createsuperuser --username admin --email admin@bookstore.com
# Password: admin123
cd ..
```

#### d. Populate sách vào Book Service
```bash
cd book-service
python3 populate_books.py
cd ..
```

## Cách chạy

### Chạy thủ công
Mở 4 tab terminal riêng biệt và chạy các lệnh sau:

**Lưu ý**: Đảm bảo đã kích hoạt virtual environment trước khi chạy:
```bash
source /Users/huynq/Workspace/python/kttkpm/Assignment_01_v3/micro/venv/bin/activate
```

**Terminal 1 - Customer Service:**
```bash
cd /Users/huynq/Workspace/python/kttkpm/Assignment_01_v3/micro/customer-service
python3 manage.py runserver 8002
```

**Terminal 2 - Book Service:**
```bash
cd /Users/huynq/Workspace/python/kttkpm/Assignment_01_v3/micro/book-service
python3 manage.py runserver 8003
```

**Terminal 3 - Cart Service:**
```bash
cd /Users/huynq/Workspace/python/kttkpm/Assignment_01_v3/micro/cart-service
python3 manage.py runserver 8004
```

**Terminal 4 - Gateway:**
```bash
cd /Users/huynq/Workspace/python/kttkpm/Assignment_01_v3/micro/gateway
python3 manage.py runserver 8005
```

## Truy cập hệ thống

### Web Application
**URL**: http://localhost:8005/

### Django Admin Panels
- **Customer Service**: http://localhost:8002/admin/
  - Username: admin@bookstore.com
  - Password: admin123

- **Book Service**: http://localhost:8003/admin/
  - Username: admin
  - Password: admin123

- **Cart Service**: http://localhost:8004/admin/
  - Username: admin
  - Password: admin123

### REST APIs
- **Customer API**: http://localhost:8002/api/customers/
- **Book API**: http://localhost:8003/api/books/
- **Cart API**: http://localhost:8004/api/carts/

