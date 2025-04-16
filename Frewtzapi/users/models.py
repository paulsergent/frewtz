from django.db import models
from .manager import CustomUserManager
from django.contrib.auth.models import AbstractUser #AbstractUser is a built-in Django model that provides a base class for creating custom user models. it contains fields like username, email, first_name, last_name, password, etc.


class User(AbstractUser):
    ROLE_CHOICES = (
        ('farmer', 'Farmer'),
        ('customer', 'Customer'),
        #('admin', 'Admin')
    )
    username = None
    first_name = models.CharField(max_length=100, default='', blank=True, null=True) # First name field with a maximum length of 100 characters, default value of an empty string, and allows blank and null values.
    last_name = models.CharField(max_length=100, default='', blank=True, null=True) # Last name field with a maximum length of 100 characters, default value of an empty string, and allows blank and null values.
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, default='', blank=True, null=True) # Phone number field with a maximum length of 15 characters, default value of an empty string, and allows blank and null values.
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='customer')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [] # This field is used to specify the unique identifier for the user model. In this case, it is set to 'email', which means that the email field will be used as the unique identifier for authentication purposes. The REQUIRED_FIELDS list is empty, indicating that no additional fields are required when creating a user.

    objects = CustomUserManager() # Custom user manager class for the custom user model Product, which is used to create and manage user instances. if you don't put it, then it will use the default user manager class, which is not compatible with the custom user model. The default user manager class contains methods for creating and managing user instances, such as create_user() and create_superuser().
    def __str__(self): # This method returns the email of the user and creates a name-tag for this model
        return self.email
    
    