# Monolithic Architecture - BookStore

## Yêu cầu
- Python 3.8+
- MySQL 8.0+

## Cài đặt & Chạy

### 1. Tạo môi trường ảo
```bash
python3 -m venv venv
source venv/bin/activate
```

### 2. Cài đặt dependencies
```bash
pip install -r requirements.txt
```

### 3. Tạo database MySQL
```sql
CREATE DATABASE monolith_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 4. Cấu hình database
Sửa file `bookstore/settings.py`:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'monolith_db',
        'USER': 'root',
        'PASSWORD': 'your_password',  # Thay đổi
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```

### 5. Chạy migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Tạo superuser
```bash
python manage.py createsuperuser
```

### 7. Chạy server
```bash
python manage.py runserver 8000
```

Truy cập: http://localhost:8000/

## Cấu trúc thư mục
```
monolith/
├── manage.py
├── requirements.txt
├── bookstore/           # Django project settings
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── accounts/            # Quản lý người dùng
│   ├── models.py        # Customer model
│   ├── views.py
│   └── urls.py
├── books/               # Quản lý sách
│   ├── models.py        # Book model
│   ├── views.py
│   └── urls.py
├── cart/                # Quản lý giỏ hàng
│   ├── models.py        # Cart, CartItem models
│   ├── views.py
│   └── urls.py
└── templates/           # HTML templates
```

## URLs chính
| URL | Mô tả |
|-----|-------|
| `/` | Trang chủ |
| `/accounts/register/` | Đăng ký |
| `/accounts/login/` | Đăng nhập |
| `/books/` | Danh sách sách |
| `/cart/` | Giỏ hàng |
| `/admin/` | Django Admin |
