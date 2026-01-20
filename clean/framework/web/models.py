# Import models from infrastructure layer to register with Django
from infrastructure.django_models import CustomerModel, BookModel, CartModel, CartItemModel

# Re-export them so Django can discover them
__all__ = ['CustomerModel', 'BookModel', 'CartModel', 'CartItemModel']

