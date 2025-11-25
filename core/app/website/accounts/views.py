from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import login, logout
from app.accounts.models import UserProfile, User, PhoneOTP
from app.website.accounts.forms import UserProfileForm, UserRegisterForm, SetPasswordForm
from app.website.accounts.scripts import send_bulk_sms
import random

@login_required
def profile_view(request):
    
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    return render(request, "accounts/profile_view.html", {"profile": profile})


@login_required
def profile_edit(request):

    profile, created = UserProfile.objects.get_or_create(user=request.user)
    user = request.user   

    if request.method == "POST":

        form = UserProfileForm(request.POST, instance=profile)

        if form.is_valid():

            form.save()

            user.first_name = request.POST.get("first_name")
            user.last_name = request.POST.get("last_name")
            user.save()

            return redirect("website_accounts:profile_view")

    else:
        form = UserProfileForm(instance=profile)

    return render(request, "accounts/profile_edit.html", {
        "form": form,
        "user": user,
    })

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
            return redirect("home")
    else:
        form = SetPasswordForm()

    return render(request, "accounts/set_password.html", {"form": form})

def logout_view(request):
    logout(request) 
    messages.success(request, "شما با موفقیت خارج شدید.")
    return redirect("home")