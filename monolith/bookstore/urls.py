from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from rest_framework.routers import DefaultRouter
from accounts.api_views import CustomerViewSet
from books.api_views import BookViewSet
from cart.api_views import CartViewSet, CartItemViewSet

# API Router
router = DefaultRouter()
router.register(r'customers', CustomerViewSet, basename='customer')
router.register(r'books', BookViewSet, basename='book')
router.register(r'carts', CartViewSet, basename='cart')
router.register(r'cart-items', CartItemViewSet, basename='cartitem')

urlpatterns = [
    path('', RedirectView.as_view(url='/books/', permanent=False), name='home'),
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('books/', include('books.urls')),
    path('cart/', include('cart.urls')),
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls')),
]