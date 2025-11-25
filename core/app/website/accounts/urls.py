from django.urls import path, include
from django.conf import settings
from app.website.accounts.views import profile_view, profile_edit, register_view, verify_otp, set_password, logout_view

app_name = "website_accounts"

urlpatterns = [
    path("register/", register_view, name="register"),
    path("verify_otp/", verify_otp, name="verify_otp"),
    path("set-password/", set_password, name="set_password"),
    path("profile/", profile_view, name="profile_view"),
    path("profile/edit/", profile_edit, name="profile_edit"),
    path("logout/", logout_view, name="logout"),
]