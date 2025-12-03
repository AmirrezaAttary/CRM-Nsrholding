from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from app.website.models import (
    News, PurchaseLivestock, OrganicProducts, AnimalFeedKhoshab,
    MotherChickenFarm, layingHen, SupplyingLivestock,
    AnimalRefinery, PlantRefinery
)

class StaticViewSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.8

    def items(self):
        
        return ['home', 'about', 'contact', 'investment', 'animal_feed']

    def location(self, item):
        return reverse(item)


class NewsSitemap(Sitemap):
    changefreq = "daily"
    priority = 1.0

    def items(self):
        return News.objects.filter(is_active=True)

    def lastmod(self, obj):
        return obj.published_date


class PurchaseLivestockSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8

    def items(self):
        return PurchaseLivestock.objects.all().order_by('-published_date')

    def lastmod(self, obj):
        return obj.published_date

class OrganicProductsSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8

    def items(self):
        return OrganicProducts.objects.all().order_by('-published_date')

    def lastmod(self, obj):
        return obj.published_date


class AnimalFeedKhoshabSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.6

    def items(self):
        return AnimalFeedKhoshab.objects.all().order_by('-published_date')

    def lastmod(self, obj):
        return obj.published_date

class MotherChickenFarmSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.6

    def items(self):
        return MotherChickenFarm.objects.all().order_by('-published_date')

    def lastmod(self, obj):
        return obj.published_date


class LayingHenSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.6

    def items(self):
        return layingHen.objects.all().order_by('-published_date')

    def lastmod(self, obj):
        return obj.published_date


class SupplyingLivestockSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.6

    def items(self):
        return SupplyingLivestock.objects.all().order_by('-published_date')

    def lastmod(self, obj):
        return obj.published_date


# -------------------
class AnimalRefinerySitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.5

    def items(self):
        return AnimalRefinery.objects.all().order_by('-published_date')

    def lastmod(self, obj):
        return obj.published_date


class PlantRefinerySitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.5

    def items(self):
        return PlantRefinery.objects.all()

    def lastmod(self, obj):
        return obj.published_date