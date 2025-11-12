from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django_jalali.db import models as jmodels
from app.accounts.validators import validate_iranian_cellphone_number


class UserType(models.IntegerChoices):
    KARSHENAS_FOROOSH = 1, _("کارشناس فروش")
    HESABDAR = 2, _("حسابدار")
    SUPERUSER = 3, _("سوپر یوزر")
    MODIR_FOROOSH = 4, _("مدیر فروش")
    SARPARAST_TEAM = 5, _("سرپرست تیم")
    MODIR_AMEL = 6, _("مدیر عامل")


class UserManager(BaseUserManager):
    """
    Custom user model manager where phone_number is the unique identifier
    for authentication instead of username/email.
    """

    def create_user(self, phone_number, password=None, **extra_fields):
        """
        Create and save a User with the given phone number and password.
        """
        if not phone_number:
            raise ValueError(_("The phone number must be set"))
        user = self.model(phone_number=phone_number, **extra_fields)
        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, password=None, **extra_fields):
        """
        Create and save a SuperUser with the given phone number and password.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)  
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("is_verified", True)
        extra_fields.setdefault("type", UserType.SUPERUSER.value)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))
        return self.create_user(phone_number, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    phone_number = models.CharField(
        max_length=12,
        unique=True,
        validators=[validate_iranian_cellphone_number],
    )
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)
    type = models.IntegerField(
        choices=UserType.choices, default=UserType.KARSHENAS_FOROOSH.value
    )

    created_date = jmodels.jDateField(auto_now_add=True,blank=True,null=True)
    updated_date = jmodels.jDateField(auto_now=True,blank=True,null=True)

    USERNAME_FIELD = "phone_number"
    REQUIRED_FIELDS = []  
    objects = UserManager()

    def __str__(self):
        return str(self.phone_number)

    class Meta:
        ordering = ["-id"]