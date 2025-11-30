from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from urllib3 import request
from app.accounts.models import UserProfile, User, PhoneOTP
from app.website.accounts.forms import (UserProfileForm, UserRegisterForm, SetPasswordForm,
                                         LoginForm, OTPLoginForm, OTPVerifyForm)
from app.website.accounts.scripts import send_bulk_sms
import random

@login_required
def profile_view(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)

    return render(request, "accounts/profile_view.html", {
        "profile": profile,
        "user": request.user
    })


@login_required
def profile_edit(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    user = request.user

    if request.method == "POST":
        form = UserProfileForm(request.POST, instance=profile)

        if form.is_valid():
            form.save()

            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.save()

            return redirect("website_accounts:profile_view")

    else:
        form = UserProfileForm(
            instance=profile,
            initial={
                "first_name": user.first_name,
                "last_name": user.last_name,
            }
        )

    return render(request, "accounts/profile_edit.html", {
        "form": form,
        "user": user,          
        "profile": profile,
    })

@login_required
def profile_delete(request):
    profile = request.user.profile

    if request.method == "POST":
        profile.delete()
        return redirect("home")

    return redirect("website_accounts:profile_edit")

def register_view(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            phone = form.cleaned_data["phone_number"]
            otp_code = str(random.randint(10000, 99999))
            PhoneOTP.objects.create(phone=phone, code=otp_code)
            send_bulk_sms(
                message_text=f"کد تایید شما: {otp_code}",
                mobiles=[phone]
            )

            request.session["temp_user_data"] = {"phone_number": phone}  
            request.session["otp_phone"] = phone
            
            return redirect("website_accounts:verify_otp")
    else:
        form = UserRegisterForm()

    return render(request, "accounts/register.html", {"form": form})

def verify_otp(request):
    phone = request.session.get("otp_phone")

    if request.method == "POST":
        entered_code = request.POST.get("code")

        otp_obj = PhoneOTP.objects.filter(phone=phone).last()

        if otp_obj is None:
            messages.error(request, "کدی یافت نشد.")
            return redirect("website_accounts:register")

        if otp_obj.is_expired():
            messages.error(request, "کد منقضی شده است.")
            return redirect("website_accounts:register")

        if otp_obj.code == entered_code:
            return redirect("website_accounts:set_password")

        else:
            messages.error(request, "کد اشتباه است.")

    return render(request, "accounts/verify_otp.html")

def set_password(request):
   
    phone = request.session.get("otp_phone")
    temp_data = request.session.get("temp_user_data")

    if not phone or not temp_data:
        messages.error(request, "لطفا ابتدا ثبت‌نام و تایید OTP را انجام دهید.")
        return redirect("website_accounts:register")

    if request.method == "POST":
        form = SetPasswordForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data["password"]

            
            user = User.objects.create_user(
                phone_number=temp_data["phone_number"], 
                password=password
            )

           
            request.session.pop("otp_phone")
            request.session.pop("temp_user_data")
            
            login(request, user)
            

            messages.success(request, "حساب شما با موفقیت فعال شد.")
            return redirect("/")
    else:
        form = SetPasswordForm()

    return render(request, "accounts/set_password.html", {"form": form})

def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)

        if form.is_valid():
            phone = form.cleaned_data["phone_number"]
            password = form.cleaned_data["password"]

            user = authenticate(request, phone_number=phone, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, "با موفقیت وارد شدید.")
                return redirect("/")
            else:
                messages.error(request, "شماره موبایل یا رمز عبور اشتباه است.")
    else:
        form = LoginForm()

    return render(request, "accounts/login.html", {"form": form})

def login_otp_view(request):
    if request.method == "POST":
        form = OTPLoginForm(request.POST)
        if form.is_valid():
            phone = form.cleaned_data["phone_number"]

            if not User.objects.filter(phone_number=phone).exists():
                messages.error(request, "این شماره موبایل در سیستم ثبت نشده است.")
                return redirect("website_accounts:login_with_otp")

            otp_code = str(random.randint(10000, 99999))
            PhoneOTP.objects.create(phone=phone, code=otp_code)

            send_bulk_sms(
                message_text=f"کد ورود شما: {otp_code}",
                mobiles=[phone]
            )

            request.session["otp_phone"] = phone

            return redirect("website_accounts:verify_otp_login")
    else:
        form = OTPLoginForm()

    return render(request, "accounts/login_otp.html", {"form": form})

def verify_otp_login_view(request):
    phone = request.session.get("otp_phone")
    if not phone:
        messages.error(request, "ابتدا شماره موبایل خود را وارد کنید.")
        return redirect("website_accounts:login_with_otp")

    if request.method == "POST":
        form = OTPVerifyForm(request.POST)
        if form.is_valid():
            entered_code = form.cleaned_data["otp_code"]

            otp_obj = PhoneOTP.objects.filter(phone=phone).last()
            if not otp_obj:
                messages.error(request, "کدی برای این شماره یافت نشد.")
                return redirect("website_accounts:login_with_otp")

            if otp_obj.is_expired():
                messages.error(request, "کد منقضی شده است.")
                return redirect("website_accounts:login_with_otp")

            if otp_obj.code == entered_code:
                
                user = User.objects.get(phone_number=phone)
                login(request, user)
                request.session.pop("otp_phone")

                messages.success(request, "با موفقیت وارد شدید.")
                return redirect("/")
            else:
                messages.error(request, "کد وارد شده اشتباه است.")
    else:
        form = OTPVerifyForm()

    return render(request, "accounts/verify_otp_login.html", {"form": form})



def logout_view(request):
    logout(request) 
    messages.success(request, "شما با موفقیت خارج شدید.")
    return redirect("/")