from rest_framework import permissions, exceptions
from app.accounts.models import UserType

class IsSuperUser(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            raise exceptions.AuthenticationFailed(detail="ابتدا وارد حساب کاربری خود شوید.")

        if request.user.type not in [UserType.SUPERUSER]:
            raise exceptions.PermissionDenied(detail="اجازه دسترسی ندارید. فقط ادمین اصلی مجاز است.")

        return True

class IsModirOrSuperUser(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            raise exceptions.AuthenticationFailed(detail="ابتدا وارد حساب کاربری خود شوید.")

        if request.user.type not in [UserType.SUPERUSER , UserType.MODIR_AMEL]:
            raise exceptions.PermissionDenied(detail="اجازه دسترسی ندارید. فقط ادمین اصلی و مدیرعامل مجاز است.")

        return True

