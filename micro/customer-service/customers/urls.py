from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('<int:customer_id>/', views.get_customer, name='get_customer'),
    path('', views.list_customers, name='list_customers'),
]
