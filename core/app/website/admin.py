from django.contrib import admin
from .models import News, PurchaseLivestock, OrganicProducts

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
            'fields': ('product_name', 'product_price','product_photo')
        }),
        ('زمان انتشار', {
            'fields': ('published_date',)
        }),
    )

    def __str__(self):
        return self.product_name
    
@admin.register(OrganicProducts)
class OrganicProductsAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'published_date','product_title')
    list_filter = ('published_date',)
    search_fields = ('product_name', 'product_title')
    ordering = ('-published_date',)
    date_hierarchy = 'published_date'
    list_per_page = 20

    fieldsets = (
        ('مشخصات محصول', {
            'fields': ('product_name', 'product_title', 'product_photo')
        }),
        ('زمان انتشار', {
            'fields': ('published_date',)
        }),
    )
