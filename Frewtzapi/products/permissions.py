from rest_framework.permissions import BasePermission
from users.models import User

class IsFarmerPermission(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated and request.user.role == 'farmer':
            return True
        return False
    
    