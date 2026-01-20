"""
Django Models - Infrastructure Layer
These models implement the persistence mechanism using Django ORM
"""
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from decimal import Decimal


class CustomerManager(BaseUserManager):
    """Custom manager for Customer model"""
    
    def create_user(self, email, name, password=None):
        if not email:
            raise ValueError('Email is required')
        
        user = self.model(
            email=self.normalize_email(email),
            name=name
        )
        user.set_password(password)
        user.save(using=self._db)
        return user


class CustomerModel(AbstractBaseUser):
    """Django model for Customer entity"""
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    
    objects = CustomerManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']
    
    class Meta:
        app_label = 'web'
        db_table = 'customers'
    
    def __str__(self):
        return self.email
    
    def has_perm(self, perm, obj=None):
        return self.is_superuser
    
    def has_module_perms(self, app_label):
        return self.is_superuser


class BookModel(models.Model):
    """Django model for Book entity"""
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField(default=0)
    
    class Meta:
        app_label = 'web'
        db_table = 'books'
    
    def __str__(self):
        return self.title


class CartModel(models.Model):
    """Django model for Cart entity"""
    customer = models.ForeignKey(CustomerModel, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        app_label = 'web'
        db_table = 'carts'
    
    def __str__(self):
        return f"Cart for {self.customer.email}"


class CartItemModel(models.Model):
    """Django model for CartItem entity"""
    cart = models.ForeignKey(CartModel, on_delete=models.CASCADE)
    book = models.ForeignKey(BookModel, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    
    class Meta:
        app_label = 'web'
        db_table = 'cart_items'
        unique_together = ('cart', 'book')
    
    def __str__(self):
        return f"{self.quantity} x {self.book.title}"
