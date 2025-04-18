from django.contrib.auth.models import BaseUserManager

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        #handle email validation
        if not email:
            raise ValueError("The Email field must be set")
        
        if "@" not in email and "." not in email:
            raise ValueError("The Email field must be valid")
        
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user
    
    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)
    

    def create_farmer(self, email, password=None, **extra_fields):
        extra_fields.setdefault('role', 'farmer')   
        return self.create_user(email, password, **extra_fields)
    def create_customer(self, email, password=None, **extra_fields):
        extra_fields.setdefault('role', 'customer')   
        return self.create_user(email, password, **extra_fields)
    def create_admin(self, email, password=None, **extra_fields):
        extra_fields.setdefault('role', 'admin') 
        extra_fields.setdefault('is_staff', True)  
        return self.create_user(email, password, **extra_fields)
    
    