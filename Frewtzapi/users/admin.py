from django.contrib import admin
from .models import User
from django.contrib.auth.models import Group

# Register your models here.

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['id', 'email', 'password', 'role', 'phone_number', 'is_staff', 'is_superuser']
    search_fields = ['id', 'email', 'role', 'phone_number']

admin.site.register(User, CustomUserAdmin) # Registering the User model with the CustomUserAdmin class
admin.site.unregister(Group)