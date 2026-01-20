from django.urls import path
from . import views  # Import views từ app books

urlpatterns = [
    path('', views.book_list, name='book_list'),  # Route gốc cho list books (ví dụ: /books/)
]