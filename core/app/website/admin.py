from django.contrib import admin
from .models import (News, PurchaseLivestock, OrganicProducts,
                        AnimalFeedKhoshab, MotherChickenFarm, layingHen,
                          SupplyingLivestock, AnimalRefinery, PlantRefinery, Contact, ContactRequest)

@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'published_date', 'is_active')
    list_filter = ('is_active', 'published_date', 'author')
    search_fields = ('title', 'author', 'tags')
    list_editable = ('is_active',)
    ordering = ('-published_date',)
    date_hierarchy = 'published_date'
    readonly_fields = ('published_date',)
    fieldsets = (
        ('اطلاعات اصلی', {
            'fields': ('title', 'content', 'author', 'tags')
        }),
        ('تصویر و وضعیت', {
            'fields': ('image', 'is_active')
        }),
        ('زمان انتشار', {
            'fields': ('published_date',),
        }),
    )

    def get_queryset(self, request):
        """برای بهبود کارایی و ترتیب پیش‌فرض"""
        qs = super().get_queryset(request)
        return qs.select_related()

    def __str__(self):
        return self.title
    
@admin.register(PurchaseLivestock)
class PurchaseLivestockAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'product_price', 'published_date')
    list_filter = ('published_date',)
    search_fields = ('product_name',)
    ordering = ('-published_date',)
    date_hierarchy = 'published_date'
    list_per_page = 20  

    fieldsets = (
        ('اطلاعات کالا', {
            'fields': ('product_name', 'product_price','product_photo','product_description')
        }),
        ('زمان انتشار', {
            'fields': ('published_date',)
        }),
    )

    def __str__(self):
        return self.product_name
    
@admin.register(OrganicProducts)
class OrganicProductsAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'published_date','product_title','product_price')
    list_filter = ('published_date',)
    search_fields = ('product_name', 'product_title')
    ordering = ('-published_date',)
    date_hierarchy = 'published_date'
    list_per_page = 20

    fieldsets = (
        ('مشخصات محصول', {
            'fields': ('product_name', 'product_title', 'product_photo','product_price')
        }),
        ('زمان انتشار', {
            'fields': ('published_date',)
        }),
    )

@admin.register(AnimalFeedKhoshab)
class AnimalFeedKhoshabAdmin(admin.ModelAdmin):
    list_display = ('title', 'published_date')
    list_filter = ('published_date',)
    ordering = ('-published_date',)

    fieldsets = (
        ('مشخصات', {
            'fields': ('title','description', 'image')
        }),
        ('زمان انتشار', {
            'fields': ('published_date',)
        }),
    )

@admin.register(MotherChickenFarm)
class MotherChickenFarmAdmin(admin.ModelAdmin):
    list_display = ('title', 'published_date')
    list_filter = ('published_date',)
    ordering = ('-published_date',)

    fieldsets = (
        ('مشخصات', {
            'fields': ('title','description', 'image')
        }),
        ('زمان انتشار', {
            'fields': ('published_date',)
        }),
    )

@admin.register(layingHen)
class layingHenAdmin(admin.ModelAdmin):
    list_display = ('title', 'published_date')
    list_filter = ('published_date',)
    ordering = ('-published_date',)

    fieldsets = (
        ('مشخصات', {
            'fields': ('title','description', 'image')
        }),
        ('زمان انتشار', {
            'fields': ('published_date',)
        }),
    )

@admin.register(SupplyingLivestock)
class SupplyingLivestockAdmin(admin.ModelAdmin):
    list_display = ('title', 'published_date')
    list_filter = ('published_date',)
    ordering = ('-published_date',)

    fieldsets = (
        ('مشخصات', {
            'fields': ('title','description', 'image')
        }),
        ('زمان انتشار', {
            'fields': ('published_date',)
        }),
    )

@admin.register(AnimalRefinery)
class AnimalRefineryAdmin(admin.ModelAdmin):
    list_display = ('title', 'published_date')
    list_filter = ('published_date',)
    ordering = ('-published_date',)

    fieldsets = (
        ('مشخصات', {
            'fields': ('title','description', 'image')
        }),
        ('زمان انتشار', {
            'fields': ('published_date',)
        }),
    )

@admin.register(PlantRefinery)
class PlantRefineryAdmin(admin.ModelAdmin):
    list_display = ('title', 'published_date')
    list_filter = ('published_date',)
    ordering = ('-published_date',)

    fieldsets = (
        ('مشخصات', {
            'fields': ('title','description', 'image')
        }),
        ('زمان انتشار', {
            'fields': ('published_date',)
        }),
    )

@admin.register(Contact)
class ContactAdmin (admin.ModelAdmin):
    list_display = ('full_name', 'email','number','message')
    list_filter = ('email','full_name')
    readonly_fields = ('crate_deta',)
    ordering = ('-crate_deta',)

    fieldsets = (
        ('مشخصات', {
            'fields': ('full_name','email', 'number','message')
        }),
        ('زمان انتشار', {
            'fields': ('crate_deta',)
        }),
    )

@admin.register(ContactRequest)
class ContactRequestAdmin(admin.ModelAdmin):
    list_display = ("name", "number", "email", "city", "job", "capital", "created_at")
    list_filter = ("job", "capital", "city", "created_at")
    search_fields = ("name", "number", "email", "city")
    ordering = ("-created_at",)
    readonly_fields = ("created_at",)

    fieldsets = (
        ("اطلاعات کاربر", {
            "fields": ("name", "number", "email", "city")
        }),
        ("اطلاعات شغلی", {
            "fields": ("job", "capital")
        }),
        ("پیام", {
            "fields": ("message",)
        }),
        ("زمان ثبت", {
            "fields": ("created_at",),
        }),
    )