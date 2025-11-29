from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from django.contrib.sessions.models import Session
from app.accounts.models import UserProfile

User = get_user_model()


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ("id", "phone_number", "first_name", "last_name",
                    "is_superuser", "is_active", "is_verified")
    list_filter = ("is_superuser", "is_active", "is_verified", "type")
    search_fields = ("phone_number", "first_name", "last_name")
    ordering = ("-id",)

    
    readonly_fields = ("created_date", "updated_date", "last_login")

    fieldsets = (
        (
            "Authentication",
            {"fields": ("phone_number", "password")},
        ),
        (
            "Personal info",
            {"fields": ("first_name", "last_name")},
        ),
        (
            "Permissions",
            {
                "fields": (
                    "is_staff",
                    "is_active",
                    "is_superuser",
                    "is_verified",
                    "groups",
                    "user_permissions",
                    "type",
                )
            },
        ),
        (
            "Important dates",
            {
                "fields": ("last_login", "created_date", "updated_date"),
            },
        ),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "phone_number",
                    "password1",
                    "password2",
                    "first_name",
                    "last_name",
                    "is_staff",
                    "is_active",
                    "is_superuser",
                    "is_verified",
                    "type",
                ),
            },
        ),
    )

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = (
        "user",          
        "get_first_name",
        "get_last_name",
        "email",
        "code_meli",
        "job",
        "created_at",
        "updated_at",
    )
    search_fields = (
        "user__phone_number",  
        "user__first_name",
        "user__last_name",
        "email",
        "code_meli",
    )
    list_filter = ("job",)
    readonly_fields = ("created_at", "updated_at")
    fieldsets = (
        ("اطلاعات کاربر", {
            "fields": ("user", "get_first_name", "get_last_name")
        }),
        ("اطلاعات پروفایل", {
            "fields": (
                "email",
                "code_meli",
                "birth_date",
                "job",
                "code_yekta",
                "address",
                "code_posti",
            )
        }),
        ("زمان‌بندی", {
            "fields": ("created_at", "updated_at")
        }),
    )

    def get_first_name(self, obj):
        return obj.user.first_name
    get_first_name.short_description = "نام"

    def get_last_name(self, obj):
        return obj.user.last_name
    get_last_name.short_description = "نام خانوادگی"

class SessionAdmin(admin.ModelAdmin):
    def _session_data(self, obj):
        return obj.get_decoded()
    list_display = ['session_key', '_session_data', 'expire_date']
    readonly_fields = ['_session_data']
admin.site.register(Session, SessionAdmin)