from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser

class Customer(AbstractUser):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    username = None  # Sử dụng email thay username
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return self.email