from rest_framework.permissions import BasePermission
from app.accounts.models import UserType

class IsSuperUserOrKarshenasForoosh(BasePermission):
    
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and
            request.user.type in [
                UserType.SUPERUSER,
                UserType.KARSHENAS_FOROOSH
            ]
        )


class IsSuperUserOrKarshenasForooshOrModirAmel(BasePermission):
   
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and
            request.user.type in [
                UserType.SUPERUSER,
                UserType.KARSHENAS_FOROOSH,
                UserType.MODIR_AMEL
            ]
        )