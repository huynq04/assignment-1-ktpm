"""
Domain Entities - Pure Python objects without any framework dependencies
These represent the core business objects
"""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from decimal import Decimal


@dataclass
class Customer:
    """Customer entity"""
    id: Optional[int]
    name: str
    email: str
    password_hash: str
    date_joined: Optional[datetime] = None
    
    def __post_init__(self):
        if self.date_joined is None:
            self.date_joined = datetime.now()


@dataclass
class Book:
    """Book entity"""
    id: Optional[int]
    title: str
    author: str
    price: Decimal
    stock: int
    
    def is_available(self) -> bool:
        """Check if book is in stock"""
        return self.stock > 0
    
    def can_order(self, quantity: int) -> bool:
        """Check if we can order the requested quantity"""
        return self.stock >= quantity


@dataclass
class Cart:
    """Cart entity"""
    id: Optional[int]
    customer_id: int
    created_at: Optional[datetime] = None
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()


@dataclass
class CartItem:
    """Cart item entity"""
    id: Optional[int]
    cart_id: int
    book_id: int
    quantity: int
    
    def calculate_subtotal(self, book_price: Decimal) -> Decimal:
        """Calculate subtotal for this cart item"""
        return book_price * self.quantity
