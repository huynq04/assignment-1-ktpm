from django.urls import path
from . import views

urlpatterns = [
    path('', views.list_books, name='list_books'),
    path('<int:book_id>/', views.get_book, name='get_book'),
    path('<int:book_id>/stock/', views.update_stock, name='update_stock'),
]
