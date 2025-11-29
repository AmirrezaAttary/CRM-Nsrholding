from django import forms
from app.accounts.models import UserProfile


class UserRegisterForm(forms.Form):
    phone_number = forms.CharField(max_length=12)

class VerifyOTPForm(forms.Form):
    code = forms.CharField(max_length=6)

class SetPasswordForm(forms.Form):
    password = forms.CharField(min_length=8, widget=forms.PasswordInput())

class UserProfileForm(forms.ModelForm):
    
    first_name = forms.CharField(
        max_length=50,
        required=False,
    )
    last_name = forms.CharField(
        max_length=50,
        required=False,
    )

    class Meta:
        model = UserProfile
        fields = [
            "first_name",
            "last_name",
            "email",
            "code_meli",
            "birth_date",
            "job",
            "code_yekta",
            "address",
            "code_posti",
        ]
    
class LoginForm (forms.Form):
    phone_number = forms.CharField(max_length=12)
    password = forms.CharField(widget=forms.PasswordInput())

class OTPLoginForm(forms.Form):
    phone_number = forms.CharField(max_length=12)

class OTPVerifyForm(forms.Form):
    otp_code = forms.CharField(max_length=6)


