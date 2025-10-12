from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.db.models import Q
from .models import CallReport, FieldActivity, ValidationLevel, CargoAnnouncement, ProductType, PortName, CountryName, LoadingTime
from django_jalali.admin.filters import JDateFieldListFilter
from django_jalali.admin.widgets import AdminjDateWidget

######################
# admin panel Call Report

class FieldActivityAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent')  
    search_fields = ('name',)          
    list_filter = ('parent',)          
    ordering = ('parent', 'name') 

class CallReportAdmin(admin.ModelAdmin):
    list_display = ('number', 'name', 'field_activity', 'province', 'city', 'purchase_satisfaction', 'validation', 'last_purchase')
    list_filter = ('field_activity', 'province', 'city', 'purchase_satisfaction', 'validation')
    search_fields = ('number', 'name', 'province', 'city')
    ordering = ('-number',)
    widgets = {
            'last_purchase': AdminjDateWidget,
        }

class ValidationLevelAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent')  
    search_fields = ('name',)          
    list_filter = ('parent',)          
    ordering = ('parent', 'name') 

##################################

# Original Admin Panel Cargo Announcement

class CargoAnnouncementAdmin(admin.ModelAdmin):
    list_display = ("load_type", "display_name", "product_type","port_name","country_name","loading_time")
    list_filter = ("load_type", "product_type","port_name","country_name","loading_time")
    search_fields = ("full_name", "name_company", "name_ceo","port_name","country_name","loading_time")
    ordering = ("load_type", "product_type")

    fieldsets = (
        (_("Load Type"), {
            "fields": ("load_type",)
        }),
        (_("Personal Information"), {
            "fields": ("full_name", "number"),
            "classes": ("collapse",)
        }),
        (_("Company Information"), {
            "fields": ("name_company", "name_ceo", "number_ceo"),
            "classes": ("collapse",)
        }),
        (_("Brand Name Information"), {
            "fields": ("product_type",)
        }),
        (_("Port Name Information"), {
            "fields": ("port_name",)
        }),
        (_("Country Name Information"), {
            "fields": ("country_name",)
        }),
        (_("Loading Time Information"), {
            "fields": ("loading_time",)
        }),
    )

    def display_name(self, obj):
        if obj.load_type == obj.LoadType.COMPANY and obj.name_company:
            return obj.name_company
        return obj.full_name or "-"
    display_name.short_description = _("Name")

# admin panel Product Type
class ProductTypeAdmin(admin.ModelAdmin):
    list_display = ("name", "parent")
    list_filter = ("parent",)
    search_fields = ("name",)
    ordering = ("parent__name", "name")
    verbose_name = _("Product Type")

    fieldsets = (
        (_("Product Type Information"), {
            "fields": ("name", "parent")
        }),
    )

# admin panel Port Name
class PortNameAdmin(admin.ModelAdmin):
    list_display = ("name", "parent")
    list_filter = ("parent",)
    search_fields = ("name",)
    ordering = ("parent__name", "name")
    verbose_name = _("Port Name")

    fieldsets = (
        (_("Port Name Information"), {
            "fields": ("name", "parent")
        }),
    )

# admin panel Country Name
class CountryNameAdmin (admin.ModelAdmin):
    list_display = ("name", "parent")
    list_filter = ("parent",)
    search_fields = ("name",)
    ordering = ("parent__name", "name")
    verbose_name = _("Port Name")

    fieldsets = (
        (_("Country Name Information"), {
            "fields": ("name", "parent")
        }),
    )


# admin panel Loading Time
class LoadingTimeAdmin (admin.ModelAdmin):
    list_display = ("name", "parent")
    list_filter = ("parent",)
    search_fields = ("name",)
    ordering = ("parent__name", "name")
    verbose_name = _("Port Name")

    fieldsets = (
        (_("Loading Time Information"), {
            "fields": ("name", "parent")
        }),
    )

admin.site.register(FieldActivity, FieldActivityAdmin)
admin.site.register(CallReport, CallReportAdmin)
admin.site.register(ValidationLevel,ValidationLevelAdmin)
admin.site.register(ProductType,ProductTypeAdmin)
admin.site.register(CargoAnnouncement,CargoAnnouncementAdmin)
admin.site.register(PortName,PortNameAdmin)
admin.site.register(CountryName,CountryNameAdmin)
admin.site.register(LoadingTime,LoadingTimeAdmin)