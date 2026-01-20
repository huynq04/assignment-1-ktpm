"""
Repository Implementations using Django ORM
These classes implement the interfaces defined in the interfaces layer
"""
from typing import List, Optional
from domain.entities import Customer, Book, Cart, CartItem
from interfaces.repositories import (
    ICustomerRepository, IBookRepository,
    ICartRepository, ICartItemRepository
)
from infrastructure.django_models import (
    CustomerModel, BookModel, CartModel, CartItemModel
)
from django.contrib.auth.hashers import make_password, check_password
from decimal import Decimal


class DjangoCustomerRepository(ICustomerRepository):
    """Django implementation of Customer repository"""
    
    def _to_entity(self, model: CustomerModel) -> Customer:
        """Convert Django model to domain entity"""
        return Customer(
            id=model.id,
            name=model.name,
            email=model.email,
            password_hash=model.password,
            date_joined=model.date_joined
        )
    
    def create(self, customer: Customer) -> Customer:
        """Create a new customer"""
        model = CustomerModel(
            name=customer.name,
            email=customer.email,
            password=make_password(customer.password_hash)
        )
        model.save()
        return self._to_entity(model)
    
    def get_by_id(self, customer_id: int) -> Optional[Customer]:
        """Get customer by ID"""
        try:
            model = CustomerModel.objects.get(id=customer_id)
            return self._to_entity(model)
        except CustomerModel.DoesNotExist:
            return None
    
    def get_by_email(self, email: str) -> Optional[Customer]:
        """Get customer by email"""
        try:
            model = CustomerModel.objects.get(email=email)
            return self._to_entity(model)
        except CustomerModel.DoesNotExist:
            return None
    
    def email_exists(self, email: str) -> bool:
        """Check if email exists"""
        return CustomerModel.objects.filter(email=email).exists()
    
    def authenticate(self, email: str, password: str) -> Optional[Customer]:
        """Authenticate user"""
        try:
            model = CustomerModel.objects.get(email=email)
            if check_password(password, model.password):
                return self._to_entity(model)
        except CustomerModel.DoesNotExist:
            pass
        return None


class DjangoBookRepository(IBookRepository):
    """Django implementation of Book repository"""
    
    def _to_entity(self, model: BookModel) -> Book:
        """Convert Django model to domain entity"""
        return Book(
            id=model.id,
            title=model.title,
            author=model.author,
            price=Decimal(str(model.price)),
            stock=model.stock
        )
    
    def get_all(self) -> List[Book]:
        """Get all books"""
        models = BookModel.objects.all()
        return [self._to_entity(m) for m in models]
    
    def get_by_id(self, book_id: int) -> Optional[Book]:
        """Get book by ID"""
        try:
            model = BookModel.objects.get(id=book_id)
            return self._to_entity(model)
        except BookModel.DoesNotExist:
            return None
    
    def create(self, book: Book) -> Book:
        """Create a new book"""
        model = BookModel(
            title=book.title,
            author=book.author,
            price=book.price,
            stock=book.stock
        )
        model.save()
        return self._to_entity(model)
    
    def update(self, book: Book) -> Book:
        """Update existing book"""
        model = BookModel.objects.get(id=book.id)
        model.title = book.title
        model.author = book.author
        model.price = book.price
        model.stock = book.stock
        model.save()
        return self._to_entity(model)
    
    def search(self, query: str) -> List[Book]:
        """Search books by title or author"""
        models = BookModel.objects.filter(
            title__icontains=query
        ) | BookModel.objects.filter(
            author__icontains=query
        )
        return [self._to_entity(m) for m in models]


class DjangoCartRepository(ICartRepository):
    """Django implementation of Cart repository"""
    
    def _to_entity(self, model: CartModel) -> Cart:
        """Convert Django model to domain entity"""
        return Cart(
            id=model.id,
            customer_id=model.customer_id,
            created_at=model.created_at
        )
    
    def get_by_customer_id(self, customer_id: int) -> Optional[Cart]:
        """Get cart by customer ID"""
        try:
            model = CartModel.objects.get(customer_id=customer_id)
            return self._to_entity(model)
        except CartModel.DoesNotExist:
            return None
    
    def create(self, cart: Cart) -> Cart:
        """Create a new cart"""
        model = CartModel(customer_id=cart.customer_id)
        model.save()
        return self._to_entity(model)
    
    def get_or_create(self, customer_id: int) -> Cart:
        """Get existing cart or create new one"""
        model, _ = CartModel.objects.get_or_create(customer_id=customer_id)
        return self._to_entity(model)


class DjangoCartItemRepository(ICartItemRepository):
    """Django implementation of CartItem repository"""
    
    def _to_entity(self, model: CartItemModel) -> CartItem:
        """Convert Django model to domain entity"""
        return CartItem(
            id=model.id,
            cart_id=model.cart_id,
            book_id=model.book_id,
            quantity=model.quantity
        )
    
    def get_by_cart_id(self, cart_id: int) -> List[CartItem]:
        """Get all items in a cart"""
        models = CartItemModel.objects.filter(cart_id=cart_id)
        return [self._to_entity(m) for m in models]
    
    def get_by_cart_and_book(self, cart_id: int, book_id: int) -> Optional[CartItem]:
        """Get specific item in cart"""
        try:
            model = CartItemModel.objects.get(cart_id=cart_id, book_id=book_id)
            return self._to_entity(model)
        except CartItemModel.DoesNotExist:
            return None
    
    def create(self, cart_item: CartItem) -> CartItem:
        """Add item to cart"""
        model = CartItemModel(
            cart_id=cart_item.cart_id,
            book_id=cart_item.book_id,
            quantity=cart_item.quantity
        )
        model.save()
        return self._to_entity(model)
    
    def update(self, cart_item: CartItem) -> CartItem:
        """Update cart item"""
        model = CartItemModel.objects.get(id=cart_item.id)
        model.quantity = cart_item.quantity
        model.save()
        return self._to_entity(model)
    
    def delete(self, cart_item_id: int) -> None:
        """Remove item from cart"""
        CartItemModel.objects.filter(id=cart_item_id).delete()
    
    def clear_cart(self, cart_id: int) -> None:
        """Remove all items from cart"""
        CartItemModel.objects.filter(cart_id=cart_id).delete()
