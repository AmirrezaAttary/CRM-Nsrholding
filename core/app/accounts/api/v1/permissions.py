from rest_framework import permissions
from app.accounts.models import UserType

class IsSuperUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and 
            request.user.type in [UserType.SUPERUSER]
        )

class IsModirOrSuperUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and 
            request.user.type in [UserType.SUPERUSER , UserType.MODIR_AMEL]
        )