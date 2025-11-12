from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator

from .models import News, PurchaseLivestock, OrganicProducts

# Create your views here.

def index_view(request):
    return render(request, 'index.html')

def about_view(request):
    return render(request, 'about.html')

def contact_view(request):
    return render(request, 'contact.html')

def location_view(request):
    return render(request, 'location.html')

def rooms_view(request):
    return render(request, 'rooms.html')

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