# ASSIGNMENT 01 - SOFTWARE ARCHITECTURE AND DESIGN
## BookStore Application - 3 Architectural Styles

## 📋 Mô tả
Project này xây dựng cùng một ứng dụng BookStore theo **3 kiến trúc khác nhau**:
- **Version A**: Monolithic Architecture
- **Version B**: Clean Architecture  
- **Version C**: Microservices Architecture

## 🎯 Chức năng chính
Cả 3 phiên bản đều có các tính năng giống hệt nhau:
- 👤 Đăng ký / Đăng nhập / Đăng xuất người dùng
- 📚 Xem danh sách sách
- 🛒 Thêm sách vào giỏ hàng
- 👁️ Xem giỏ hàng
- ✏️ Cập nhật số lượng sản phẩm trong giỏ
- 🗑️ Xóa sản phẩm khỏi giỏ
- 🔐 Django Admin panel

## 📂 Cấu trúc thư mục

```
assignment_01/
├── monolith/                 # Version A - Monolithic
│   ├── README.md            # Hướng dẫn chi tiết
│   ├── requirements.txt
│   ├── manage.py
│   ├── bookstore/           # Django project settings
│   ├── accounts/            # User management app
│   ├── books/               # Book management app
│   ├── cart/                # Cart management app
│   └── templates/           # HTML templates
│
├── clean/                    # Version B - Clean Architecture
│   ├── README.md            # Hướng dẫn chi tiết
│   ├── requirements.txt
│   ├── domain/              # Domain entities (pure Python)
│   ├── usecases/            # Business logic
│   ├── interfaces/          # Repository interfaces
│   ├── infrastructure/      # Django models & repositories
│   └── framework/           # Django web layer
│
└── micro/                    # Version C - Microservices
    ├── README.md            # Hướng dẫn chi tiết
    ├── requirements.txt
    ├── start_all_services.bat
    ├── customer-service/    # Customer microservice (Port 8002)
    ├── book-service/        # Book microservice (Port 8003)
    ├── cart-service/        # Cart microservice (Port 8004)
    └── gateway/             # Web gateway (Port 8005)
```

## 🚀 Quick Start

### Version A - Monolithic (Port 8000)
```bash
cd monolith
pip install -r requirements.txt

# Tạo database
mysql -u root -p
CREATE DATABASE monolith_db;
exit

# Setup và chạy
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver 8000
```
**Truy cập**: http://localhost:8000/

### Version B - Clean Architecture (Port 8001)
```bash
cd clean
pip install -r requirements.txt

# Tạo database
mysql -u root -p
CREATE DATABASE clean_db;
exit

# Setup và chạy
cd framework
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver 8001
```
**Truy cập**: http://localhost:8001/

### Version C - Microservices (Port 8005)
```bash
cd micro
pip install -r requirements.txt

# Tạo databases
mysql -u root -p
CREATE DATABASE customer_db;
CREATE DATABASE book_db;
CREATE DATABASE cart_db;
exit

# Migrate tất cả services
cd customer-service && python manage.py migrate && cd ..
cd book-service && python manage.py migrate && cd ..
cd cart-service && python manage.py migrate && cd ..
cd gateway && python manage.py migrate && cd ..

# Chạy tất cả services
start_all_services.bat
```
**Truy cập**: http://localhost:8005/

## 📊 So sánh các kiến trúc

| Tiêu chí | Monolithic | Clean Architecture | Microservices |
|----------|-----------|-------------------|---------------|
| **Complexity** | ⭐ Đơn giản | ⭐⭐ Trung bình | ⭐⭐⭐ Phức tạp |
| **Deployment** | 1 ứng dụng | 1 ứng dụng | 4 services riêng biệt |
| **Database** | 1 database | 1 database | 3 databases độc lập |
| **Scalability** | Scale toàn bộ | Scale toàn bộ | Scale từng service |
| **Technology** | 1 tech stack | 1 tech stack | Đa dạng tech stack |
| **Testing** | Khó test riêng logic | Dễ test từng layer | Dễ test từng service |
| **Maintenance** | Tight coupling | Loose coupling | Very loose coupling |
| **Dev Speed** | ⚡ Nhanh nhất | ⚡⚡ Trung bình | ⚡⚡⚡ Chậm ban đầu |
| **Network** | No overhead | No overhead | API calls overhead |

### Monolithic Architecture
**✅ Ưu điểm:**
- Đơn giản, dễ phát triển và deploy
- Không có network latency
- Dễ debug
- Hiệu suất cao cho small-medium apps

**❌ Nhược điểm:**
- Tight coupling giữa các module
- Khó scale theo từng phần
- Deploy toàn bộ khi có thay đổi nhỏ
- Khó áp dụng công nghệ mới

**🎯 Phù hợp:**
- Startup, MVP
- Team nhỏ
- Ứng dụng đơn giản đến trung bình

### Clean Architecture
**✅ Ưu điểm:**
- Tách biệt rõ ràng business logic và framework
- Dễ test từng layer
- Dễ thay đổi framework hoặc database
- Code maintainable, SOLID principles

**❌ Nhược điểm:**
- Learning curve cao hơn
- Nhiều boilerplate code
- Phức tạp cho small projects
- Vẫn là monolithic về deployment

**🎯 Phù hợp:**
- Enterprise applications
- Long-term projects
- Team muốn code quality cao
- Ứng dụng có business logic phức tạp

### Microservices Architecture
**✅ Ưu điểm:**
- Scale từng service độc lập
- Technology independence
- Fault isolation (1 service lỗi không ảnh hưởng toàn bộ)
- Deploy độc lập từng service
- Team có thể làm việc độc lập

**❌ Nhược điểm:**
- Infrastructure phức tạp
- Network latency
- Distributed system complexity
- Khó debug và monitor
- Data consistency challenges

**🎯 Phù hợp:**
- Large-scale applications
- Team lớn, nhiều teams
- Cần scale cao
- Công ty có DevOps mature

## 🛠️ Technology Stack

### Common (Cả 3 versions)
- **Language**: Python 3.8+
- **Framework**: Django 5.2.10
- **Database**: MySQL 8.0
- **Template Engine**: Django Templates
- **Authentication**: Django AbstractBaseUser

### Additional (Microservices)
- **REST API**: Django REST Framework 3.16.1
- **CORS**: django-cors-headers 4.6.0
- **HTTP Client**: requests 2.32.3
- **Pattern**: API Gateway

## 📦 Dependencies

### Monolithic & Clean
```
Django==5.2.10
mysqlclient==2.2.8
```

### Microservices (additional)
```
djangorestframework==3.16.1
django-cors-headers==4.6.0
requests==2.32.3
```

## 🗄️ Database Schema

### Customer/User
```sql
- id (PK)
- name
- email (unique)
- password (hashed)
```

### Book
```sql
- id (PK)
- title
- author
- price
- stock
```

### Cart
```sql
- id (PK)
- customer_id (FK)
- created_at
```

### CartItem
```sql
- id (PK)
- cart_id (FK)
- book_id (FK)
- quantity
```

## 🌐 Ports Summary
- **Monolithic**: http://localhost:8000/
- **Clean Architecture**: http://localhost:8001/
- **Microservices**:
  - Customer Service: http://localhost:8002/
  - Book Service: http://localhost:8003/
  - Cart Service: http://localhost:8004/
  - Gateway (Web UI): http://localhost:8005/

## 📖 Sample Data
Tất cả 3 versions đều có 12 quyển sách mẫu:
1. Clean Code - Robert C. Martin - $32
2. Design Patterns - Gang of Four - $45
3. The Pragmatic Programmer - Andrew Hunt - $40
4. Introduction to Algorithms - Thomas H. Cormen - $65
5. Head First Design Patterns - Eric Freeman - $38
6. Refactoring - Martin Fowler - $42
7. Python Crash Course - Eric Matthes - $30
8. Effective Python - Brett Slatkin - $35
9. JavaScript: The Good Parts - Douglas Crockford - $28
10. You Don't Know JS - Kyle Simpson - $25
11. Eloquent JavaScript - Marijn Haverbeke - $30
12. The Art of Computer Programming - Donald Knuth - $80

## 🔧 Configuration

### MySQL Connection
Mỗi version cần cấu hình password MySQL trong file `settings.py`:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'xxx_db',
        'USER': 'root',
        'PASSWORD': 'your_mysql_password',  # THAY ĐỔI NÀY!
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```

## 📚 Documentation
Mỗi version có file README.md riêng với hướng dẫn chi tiết:
- [monolith/README.md](monolith/README.md) - Monolithic Architecture
- [clean/README.md](clean/README.md) - Clean Architecture
- [micro/README.md](micro/README.md) - Microservices Architecture

## 🎓 Learning Points

### Từ Monolithic
- Django MVT pattern
- ORM và database relationships
- Session-based authentication
- Template rendering

### Từ Clean Architecture
- SOLID principles
- Dependency Inversion Principle
- Repository Pattern
- Use Case Driven Development
- Domain-Driven Design basics

### Từ Microservices
- Service decomposition
- REST API design
- API Gateway pattern
- Distributed data management
- Service-to-service communication
- Database per service pattern

## 🚨 Troubleshooting

### MySQL Connection Error
```bash
pip install mysqlclient
# Hoặc trên Windows: pip install mysqlclient-1.4.6-cp311-cp311-win_amd64.whl
```

### Port Already in Use
```bash
# Tìm process đang dùng port
netstat -ano | findstr :8000
# Kill process
taskkill /PID <process_id> /F
```

### Migration Errors
```bash
python manage.py migrate --run-syncdb
```

## 📝 Assignment Requirements Met
✅ **3 kiến trúc khác nhau**: Monolithic, Clean, Microservices  
✅ **Chức năng giống hệt nhau**: Register, Login, Books, Cart  
✅ **Database**: MySQL cho tất cả versions  
✅ **Admin panel**: Django admin cho tất cả  
✅ **Documentation**: README chi tiết cho từng version  
✅ **Runnable**: Clone về chạy được với hướng dẫn rõ ràng  

## 👨‍💻 Author
Assignment 01 - Software Architecture and Design

## 📄 License
MIT License

---

**Happy Coding! 🚀**
