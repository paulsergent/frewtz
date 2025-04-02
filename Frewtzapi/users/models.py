from django.db import models
from .manager import CustomUserManager
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    ROLE_CHOICES = (
        ('farmer', 'Farmer'),
        ('customer', 'Customer'),
        #('admin', 'Admin')
    )
    username = None
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, blank=False, null=False, default='customer')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager() # Custom user manager class for the custom user model Product

    def __str__(self): # This method returns the email of the user and creates a name-tag for this model
        return self.email