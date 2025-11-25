from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.shortcuts import render
from django.contrib import messages
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.shortcuts import redirect
from core.settings import EMAIL_HOST_USER
from .forms import ContactForm, ContactRequestForm
from .models import (News, PurchaseLivestock, OrganicProducts, AnimalFeedKhoshab,
                      MotherChickenFarm, layingHen, SupplyingLivestock, AnimalRefinery,PlantRefinery)

# Create your views here.

def index_view(request):
    return render(request, 'index.html')

def about_view(request):
    return render(request, 'about.html')

def contact_view(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.save()  
            try:
                html_content = render_to_string("contact_email.html", {
                    "full_name": instance.full_name,
                    "email": instance.email,
                    "number": instance.number,
                    "message": instance.message,
                })

                email = EmailMultiAlternatives(
                    subject="پیام جدید از فرم تماس سایت",
                    body="یک پیام جدید دریافت شد.",
                    from_email=None,
                    to=[EMAIL_HOST_USER],
                )
                email.attach_alternative(html_content, "text/html")
                email.send()

                messages.success(request, "پیام شما با موفقیت ارسال شد!")
                
            except Exception as e:
                messages.error(request, f"ارسال ایمیل با خطا مواجه شد: {e}")

            return redirect('contact')

        else:
            messages.error(request, "فرم به درستی ارسال نشد. لطفاً دوباره تلاش کنید.")
    else:
        form = ContactForm()

    return render(request, "contact.html", {"form": form})

def investment_view(request):
    if request.method == "POST":
        form = ContactRequestForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.save()  
            try:
                html_content = render_to_string("contact_request_email.html", {
                    "name": instance.name,
                    "email": instance.email,
                    "number": instance.number,
                    "city": instance.city,
                    "job": instance.job,
                    "capital": instance.capital,
                    "message": instance.message,
                })

                email = EmailMultiAlternatives(
                    subject="پیام جدید از فرم سرمایه گذاری سایت",
                    body="یک پیام جدید دریافت شد.",
                    from_email=None,
                    to=[EMAIL_HOST_USER],
                )
                email.attach_alternative(html_content, "text/html")
                email.send()

                messages.success(request, "پیام شما با موفقیت ارسال شد!")
                
            except Exception as e:
                messages.error(request, f"ارسال ایمیل با خطا مواجه شد: {e}")

            return redirect('investment')

        else:
            messages.error(request, "فرم به درستی ارسال نشد. لطفاً دوباره تلاش کنید.")
    else:
        form = ContactRequestForm()

    return render(request, "investment.html", {"form": form})

def location_view(request):
    return render(request, 'location.html')

def rooms_view(request):
    return render(request, 'rooms.html')

def animal_feed_view(request):
    return render(request, 'animal_feed.html')


def animal_feed_khoshab_view(request):
    animal_feed_khoshab = AnimalFeedKhoshab.objects.all().order_by('-published_date')
    context = {
        'animal_feed_khoshab' : animal_feed_khoshab
    }

    return render(request, 'animal_feed_khoshab.html', context)

def mother_chicken_farm_view(request):
    mother_chicken_farm = MotherChickenFarm.objects.all().order_by('-published_date')
    context = {
        'mother_chicken_farm' : mother_chicken_farm
    }

    return render(request, 'mother_chicken_farm.html', context)

def iaying_hen_view(request):
    iaying_hen = layingHen.objects.all().order_by('-published_date')
    context = {
        'iaying_hen' : iaying_hen
    }

    return render(request, 'iaying_hen.html', context)

def supplying_livestock_view(request):
    supplying_livestock  = SupplyingLivestock.objects.all().order_by('-published_date')
    context = {
        'supplying_livestock' : supplying_livestock
    }

    return render(request, 'supplying_livestock.html', context)

def animal_refinery_view(request):
    animal_refinery  = AnimalRefinery.objects.all().order_by('-published_date')
    context = {
        'animal_refinery' : animal_refinery
    }

    return render(request, 'animal_refinery.html', context)

def plant_refinery_view(request):
    plant_refinery  = PlantRefinery.objects.all().order_by('-published_date')
    context = {
        'plant_refinery' : plant_refinery
    }

    return render(request, 'plant_refinery.html', context)

def organic_products_view(request):
    organic_products_list = OrganicProducts.objects.all().order_by('-published_date')
    paginator = Paginator(organic_products_list, 6)  
    page_number = request.GET.get('page')
    obj = paginator.get_page(page_number)

    context = {
        'obj':obj,
    }
    return render(request, 'organic_products.html', context)

def organic_products_detail(request, pk):
    organic_products = get_object_or_404(OrganicProducts, pk=pk)
    context = {
        'organic_products': organic_products
    }
    return render(request, 'organic_products_detail.html', context)

def purchase_livestock_view(request):
    purchase_livestock_list = PurchaseLivestock.objects.all().order_by('-published_date')
    paginator = Paginator(purchase_livestock_list, 6)  
    page_number = request.GET.get('page')
    obj = paginator.get_page(page_number)

    context = {
        'obj':obj,
    }
    return render(request, 'purchase_livestock.html', context)

def purchase_livestock_detail(request, pk):
    purchase_livestock = get_object_or_404(PurchaseLivestock, pk=pk)
    context = {
        'purchase_livestock': purchase_livestock
    }
    return render(request, 'purchase_livestock_detail.html', context)

def news_list(request):
    news_list = News.objects.filter(is_active=True).order_by('-published_date')
    paginator = Paginator(news_list, 6)  
    page_number = request.GET.get('page')
    obj = paginator.get_page(page_number)

    context = {
        'obj':obj,
    }
    return render(request, 'news_list.html', context)

def news_detail(request, pk):
    news = get_object_or_404(News, pk=pk, is_active=True)
    context = {
        'news': news
    }
    return render(request, 'news_detail.html', context)