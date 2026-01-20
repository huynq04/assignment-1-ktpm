"""
Use Cases - Business logic layer
Contains application-specific business rules
"""
from typing import Optional, List
from decimal import Decimal
from domain.entities import Customer, Book, Cart, CartItem
from interfaces.repositories import (
    ICustomerRepository, IBookRepository, 
    ICartRepository, ICartItemRepository
)


class RegisterCustomerUseCase:
    """Use case for registering a new customer"""
    
    def __init__(self, customer_repo: ICustomerRepository):
        self.customer_repo = customer_repo
    
    def execute(self, name: str, email: str, password: str) -> Optional[Customer]:
        """Register a new customer"""
        # Check if email already exists
        if self.customer_repo.email_exists(email):
            raise ValueError("Email already registered")
        
        # Create customer entity (password will be hashed by repository)
        customer = Customer(
            id=None,
            name=name,
            email=email,
            password_hash=password  # Pass plain password
        )
        
        # Save to repository
        return self.customer_repo.create(customer)


class LoginCustomerUseCase:
    """Use case for customer login"""
    
    def __init__(self, customer_repo: ICustomerRepository):
        self.customer_repo = customer_repo
    
    def execute(self, email: str, password: str) -> Optional[Customer]:
        """Authenticate customer"""
        return self.customer_repo.authenticate(email, password)


class ListBooksUseCase:
    """Use case for listing all books"""
    
    def __init__(self, book_repo: IBookRepository):
        self.book_repo = book_repo
    
    def execute(self) -> List[Book]:
        """Get all books"""
        return self.book_repo.get_all()


class SearchBooksUseCase:
    """Use case for searching books"""
    
    def __init__(self, book_repo: IBookRepository):
        self.book_repo = book_repo
    
    def execute(self, query: str) -> List[Book]:
        """Search books"""
        return self.book_repo.search(query)


class GetBookUseCase:
    """Use case for getting a single book"""
    
    def __init__(self, book_repo: IBookRepository):
        self.book_repo = book_repo
    
    def execute(self, book_id: int) -> Optional[Book]:
        """Get book by ID"""
        return self.book_repo.get_by_id(book_id)


class AddToCartUseCase:
    """Use case for adding a book to cart"""
    
    def __init__(
        self, 
        cart_repo: ICartRepository,
        cart_item_repo: ICartItemRepository,
        book_repo: IBookRepository
    ):
        self.cart_repo = cart_repo
        self.cart_item_repo = cart_item_repo
        self.book_repo = book_repo
    
    def execute(self, customer_id: int, book_id: int, quantity: int = 1) -> CartItem:
        """Add book to customer's cart"""
        # Get or create cart
        cart = self.cart_repo.get_or_create(customer_id)
        
        # Get book to check availability
        book = self.book_repo.get_by_id(book_id)
        if not book:
            raise ValueError("Book not found")
        
        # Check if item already in cart
        existing_item = self.cart_item_repo.get_by_cart_and_book(cart.id, book_id)
        
        if existing_item:
            # Update quantity
            new_quantity = existing_item.quantity + quantity
            if not book.can_order(new_quantity):
                raise ValueError(f"Only {book.stock} items available")
            existing_item.quantity = new_quantity
            return self.cart_item_repo.update(existing_item)
        else:
            # Create new cart item
            if not book.can_order(quantity):
                raise ValueError(f"Only {book.stock} items available")
            
            cart_item = CartItem(
                id=None,
                cart_id=cart.id,
                book_id=book_id,
                quantity=quantity
            )
            return self.cart_item_repo.create(cart_item)


class ViewCartUseCase:
    """Use case for viewing cart contents"""
    
    def __init__(
        self,
        cart_repo: ICartRepository,
        cart_item_repo: ICartItemRepository,
        book_repo: IBookRepository
    ):
        self.cart_repo = cart_repo
        self.cart_item_repo = cart_item_repo
        self.book_repo = book_repo
    
    def execute(self, customer_id: int) -> dict:
        """Get cart with items and total"""
        # Get cart
        cart = self.cart_repo.get_by_customer_id(customer_id)
        if not cart:
            return {
                'cart': None,
                'items': [],
                'total': Decimal('0.00')
            }
        
        # Get cart items
        cart_items = self.cart_item_repo.get_by_cart_id(cart.id)
        
        # Calculate total
        total = Decimal('0.00')
        items_with_books = []
        
        for item in cart_items:
            book = self.book_repo.get_by_id(item.book_id)
            if book:
                subtotal = item.calculate_subtotal(book.price)
                total += subtotal
                items_with_books.append({
                    'item': item,
                    'book': book,
                    'subtotal': subtotal
                })
        
        return {
            'cart': cart,
            'items': items_with_books,
            'total': total
        }


class RemoveFromCartUseCase:
    """Use case for removing item from cart"""
    
    def __init__(self, cart_item_repo: ICartItemRepository):
        self.cart_item_repo = cart_item_repo
    
    def execute(self, cart_item_id: int) -> None:
        """Remove item from cart"""
        self.cart_item_repo.delete(cart_item_id)


class ClearCartUseCase:
    """Use case for clearing all items from cart"""
    
    def __init__(
        self,
        cart_repo: ICartRepository,
        cart_item_repo: ICartItemRepository
    ):
        self.cart_repo = cart_repo
        self.cart_item_repo = cart_item_repo
    
    def execute(self, customer_id: int) -> None:
        """Clear all items from customer's cart"""
        cart = self.cart_repo.get_by_customer_id(customer_id)
        if cart:
            self.cart_item_repo.clear_cart(cart.id)


class UpdateCartItemQuantityUseCase:
    """Use case for updating cart item quantity"""
    
    def __init__(
        self,
        cart_item_repo: ICartItemRepository,
        book_repo: IBookRepository
    ):
        self.cart_item_repo = cart_item_repo
        self.book_repo = book_repo
    
    def execute(self, cart_item_id: int, quantity: int) -> None:
        """Update quantity of cart item"""
        if quantity <= 0:
            raise ValueError("Quantity must be greater than 0")
        
        # Get cart item
        cart_item = self.cart_item_repo.get_by_id(cart_item_id)
        if not cart_item:
            raise ValueError("Cart item not found")
        
        # Get book to check stock
        book = self.book_repo.get_by_id(cart_item.book_id)
        if not book or not book.can_order(quantity):
            raise ValueError(f"Only {book.stock if book else 0} items available")
        
        # Update quantity
        cart_item.quantity = quantity
        self.cart_item_repo.update(cart_item)
