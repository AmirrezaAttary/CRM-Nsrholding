from rest_framework.permissions import BasePermission
from rest_framework.exceptions import AuthenticationFailed

class CustomIsAuthenticated(BasePermission):
    
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            raise AuthenticationFailed(detail="ابتدا وارد حساب کاربری خود شوید.")
        return True
