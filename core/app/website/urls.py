from django.contrib import admin
from django.urls import path,include
from app.website import views


urlpatterns = [
    path("", views.index_view, name="home"),
    path("about/", views.about_view, name="about"),
    path("contact/", views.contact_view, name="contact"),
    path("location/", views.location_view, name="location"),
    path("rooms/", views.rooms_view, name="rooms"),
    path("animal_feed/", views.animal_feed_view, name="animal_feed"),
    path("investment/", views.investment_view, name="investment"),
    path("purchase_livestock/", views.purchase_livestock_view, name="purchase_livestock"),
    path('purchase_livestock/<int:pk>/', views.purchase_livestock_detail, name='purchase_livestock_detail'),
    path("organic_products/", views.organic_products_view, name="organic_products"),
    path('organic_products/<int:pk>/', views.organic_products_detail, name='organic_products_detail'),
    path('news/', views.news_list, name='news_list'),
    path('news/<int:pk>/', views.news_detail, name='news_detail'),
    path('animal_feed_khoshab/', views.animal_feed_khoshab_view, name='animal_feed_khoshab'),
    path('mother_chicken_farm/', views.mother_chicken_farm_view, name='mother_chicken_farm'),
    path('iaying_hen/', views.iaying_hen_view, name='iaying_hen'),
    path('supplying_livestock/', views.supplying_livestock_view, name='supplying_livestock'),
    path('animal_refinery/', views.animal_refinery_view, name='animal_refinery'),
    path('plant_refinery/', views.plant_refinery_view, name='plant_refinery'),
    path('user/', include('app.website.accounts.urls', namespace='website_accounts')),
]