"""
Repository Interfaces - Abstract base classes that define data access contracts
These are interfaces that will be implemented by the infrastructure layer
"""
from abc import ABC, abstractmethod
from typing import List, Optional
from domain.entities import Customer, Book, Cart, CartItem


class ICustomerRepository(ABC):
    """Interface for customer data access"""
    
    @abstractmethod
    def create(self, customer: Customer) -> Customer:
        """Create a new customer"""
        pass
    
    @abstractmethod
    def get_by_id(self, customer_id: int) -> Optional[Customer]:
        """Get customer by ID"""
        pass
    
    @abstractmethod
    def get_by_email(self, email: str) -> Optional[Customer]:
        """Get customer by email"""
        pass
    
    @abstractmethod
    def email_exists(self, email: str) -> bool:
        """Check if email already exists"""
        pass
    
    @abstractmethod
    def authenticate(self, email: str, password: str) -> Optional[Customer]:
        """Authenticate user with email and password"""
        pass


class IBookRepository(ABC):
    """Interface for book data access"""
    
    @abstractmethod
    def get_all(self) -> List[Book]:
        """Get all books"""
        pass
    
    @abstractmethod
    def get_by_id(self, book_id: int) -> Optional[Book]:
        """Get book by ID"""
        pass
    
    @abstractmethod
    def create(self, book: Book) -> Book:
        """Create a new book"""
        pass
    
    @abstractmethod
    def update(self, book: Book) -> Book:
        """Update existing book"""
        pass
    
    @abstractmethod
    def search(self, query: str) -> List[Book]:
        """Search books by title or author"""
        pass


class ICartRepository(ABC):
    """Interface for cart data access"""
    
    @abstractmethod
    def get_by_customer_id(self, customer_id: int) -> Optional[Cart]:
        """Get cart by customer ID"""
        pass
    
    @abstractmethod
    def create(self, cart: Cart) -> Cart:
        """Create a new cart"""
        pass
    
    @abstractmethod
    def get_or_create(self, customer_id: int) -> Cart:
        """Get existing cart or create new one"""
        pass


class ICartItemRepository(ABC):
    """Interface for cart item data access"""
    
    @abstractmethod
    def get_by_cart_id(self, cart_id: int) -> List[CartItem]:
        """Get all items in a cart"""
        pass
    
    @abstractmethod
    def get_by_cart_and_book(self, cart_id: int, book_id: int) -> Optional[CartItem]:
        """Get specific item in cart"""
        pass
    
    @abstractmethod
    def create(self, cart_item: CartItem) -> CartItem:
        """Add item to cart"""
        pass
    
    @abstractmethod
    def update(self, cart_item: CartItem) -> CartItem:
        """Update cart item"""
        pass
    
    @abstractmethod
    def delete(self, cart_item_id: int) -> None:
        """Remove item from cart"""
        pass
    
    @abstractmethod
    def clear_cart(self, cart_id: int) -> None:
        """Remove all items from cart"""
        pass
