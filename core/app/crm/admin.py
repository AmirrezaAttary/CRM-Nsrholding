from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.db.models import Q
from .models import *
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
    list_display = ("sales_expert_name","load_type","name_company","name_ceo", "number_ceo","port_name","country_name", "display_name", "product_type","loading_time","transaction_type","product_price","description")
    list_filter = ("sales_expert_name","load_type","name_company","name_ceo", "number_ceo", "product_type","port_name","country_name","loading_time","transaction_type","product_price","description")
    search_fields = ("sales_expert_name","full_name", "name_company", "name_ceo","number_ceo","port_name","country_name","loading_time","transaction_type","product_price","description")
    ordering = ("sales_expert_name","load_type", "product_type","name_company")

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
        (_("Transaction Type Information"), {
            "fields": ("transaction_type",)
        }),
        (_("sales expert name Information"), {
            "fields": ("sales_expert_name",)
        }),
        (_("product price Information"), {
            "fields": ("product_price",)
        }),
        (_("description Information"), {
            "fields": ("description",)
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
    verbose_name = _("Country Name")

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
    verbose_name = _("Loading Time")

    fieldsets = (
        (_("Loading Time Information"), {
            "fields": ("name", "parent")
        }),
    )

# admin panel Transaction Type
class TransactionTypeAdmin (admin.ModelAdmin):
    list_display = ("name", "parent")
    list_filter = ("parent",)
    search_fields = ("name",)
    ordering = ("parent__name", "name")
    verbose_name = _("Transaction Type")

    fieldsets = (
        (_("Transaction Type Information"), {
            "fields": ("name", "parent")
        }),
    )
########################################################
# admin panel Transaction Type 
class PurchaseProcessAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "call_report",
        "load_type",
        "market_place_type",
        "created_at",
        "updated_at",
    )
    list_filter = ("load_type", "market_place_type", "created_at")
    search_fields = (
        "call_report__name",
        "buyer_name",
        "yekta_code",
        "agreement_kotazh",
        "cash_user",
    )

    readonly_fields = ("created_at", "updated_at")

    fieldsets = (
        (_("General Info"), {
            "fields": (
                "call_report",
                "load_type",
                "market_place_type",
            )
        }),
        (_("Market Outside Details"), {
            "classes": ("collapse",),
            "fields": (
                "yekta_code",
                "market_outside_address",
                "postal_code",
                "market_outside_number",
                "buyer_name",
            )
        }),
        (_("Overhead Details"), {
            "classes": ("collapse",),
            "fields": (
                "overhead_address",
                "overhead_number",
            )
        }),
        (_("MarketPlace Agreement"), {
            "classes": ("collapse",),
            "fields": (
                "agreement_kotazh",
            )
        }),
        (_("MarketPlace Cash"), {
            "classes": ("collapse",),
            "fields": (
                "cash_user",
                "cash_password",
                "cash_kotazh",
            )
        }),
        (_("Quota Details"), {
            "classes": ("collapse",),
            "fields": (
                "destination_name",
                "quota_number",
            )
        }),
        (_("Timestamps"), {
            "fields": (
                "created_at",
                "updated_at",
            )
        }),
    )

    def get_fields(self, request, obj=None):
        
        fields = ["call_report", "load_type", "market_place_type"]

        if obj:
            # MARKET OUTSIDE
            if obj.load_type == PurchaseProcess.LoadType.MARKET_OUTSIDE:
                fields += [
                    "yekta_code",
                    "market_outside_address",
                    "postal_code",
                    "market_outside_number",
                    "buyer_name",
                ]

            # OVERHEAD
            elif obj.load_type == PurchaseProcess.LoadType.OVERHEAD:
                fields += [
                    "overhead_address",
                    "overhead_number",
                ]

            # QUOTA
            elif obj.load_type == PurchaseProcess.LoadType.QUOTA:
                fields += [
                    "destination_name",
                    "quota_number",
                ]

            # MARKET PLACE
            elif obj.load_type == PurchaseProcess.LoadType.MARKET_PLACE:
                if obj.market_place_type == PurchaseProcess.MarketPlaceType.AGREEMENT:
                    fields += ["agreement_kotazh"]
                elif obj.market_place_type == PurchaseProcess.MarketPlaceType.CASH:
                    fields += ["cash_user", "cash_password", "cash_kotazh"]

        
        fields += ["created_at", "updated_at"]
        return fields

    def get_readonly_fields(self, request, obj=None):
       
        readonly = list(self.readonly_fields)
        if obj:
            readonly.append("call_report")
        return readonly
    
##############################################################

class SaleReportAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "purchase_process",
        "sale_type",
        "sale_date",
    )
    list_filter = ("sale_type", "sale_date")
    search_fields = (
        "purchase_process__call_report__name",
        "purchase_process__buyer_name",
    )

    fieldsets = (
        (_("General Info"), {
            "fields": ("purchase_process", "sale_type", "sale_date")
        }),
    )

    readonly_fields = ("sale_date",)

    def get_fields(self, request, obj=None):
        
        return ["purchase_process", "sale_type", "sale_date"]
##############################################################

# ────────────── Inlines ──────────────
class MarketPlaceInline(admin.StackedInline):
    model = MarketPlace
    extra = 0
    readonly_fields = ('profit', 'total_amount', 'account_remaining', 'unofficial')
    fields = (
        'product_name', 'weight', 'market_price', 'purchase_price', 'selling_price', 
        'profit', 'unofficial', 'total_amount', 'deposit', 'account_remaining',
        'buyer', 'seller', 'supplier', 'supply_status', 
        'sales_expert_name', 'description', 'weight_barname'
    )

class MarketOutsideInline(admin.StackedInline):
    model = MarketOutside
    extra = 0
    readonly_fields = ('profit', 'total_amount', 'account_remaining')
    fields = (
        'product_name', 'weight', 'purchase_price', 'selling_price',
        'profit', 'total_amount', 'deposit', 'account_remaining',
        'buyer', 'seller', 'supplier', 'supply_status', 
        'sales_expert_name', 'description', 'weight_barname'
    )

class QuotaInline(admin.StackedInline):
    model = Quota
    extra = 0
    readonly_fields = ('profit', 'total_amount', 'account_remaining')
    fields = (
        'product_name', 'weight', 'purchase_price', 'selling_price',
        'profit', 'total_amount', 'deposit', 'account_remaining',
        'buyer', 'seller', 'supplier', 'supply_status',
        'sales_expert_name', 'description'
    )

class OverheadInline(admin.StackedInline):
    model = Overhead
    extra = 0
    fields = ('address', 'number')


# ────────────── SaleReport Admin ──────────────
@admin.register(SaleReport)
class SaleReportAdmin(admin.ModelAdmin):
    list_display = ('purchase_process', 'sale_type', 'sale_date')
    list_filter = ('sale_type', 'sale_date')
    search_fields = ('purchase_process__call_report__name',)
    inlines = [MarketPlaceInline, MarketOutsideInline, QuotaInline, OverheadInline]


# ────────────── SupplyStatus Admin ──────────────
@admin.register(SupplyStatus)
class SupplyStatusAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent')
    list_filter = ('parent',)
    search_fields = ('name',)



admin.site.register(FieldActivity, FieldActivityAdmin)
admin.site.register(CallReport, CallReportAdmin)
admin.site.register(ValidationLevel,ValidationLevelAdmin)
admin.site.register(ProductType,ProductTypeAdmin)
admin.site.register(CargoAnnouncement,CargoAnnouncementAdmin)
admin.site.register(PortName,PortNameAdmin)
admin.site.register(CountryName,CountryNameAdmin)
admin.site.register(LoadingTime,LoadingTimeAdmin)
admin.site.register(TransactionType, TransactionTypeAdmin)
admin.site.register(PurchaseProcess,PurchaseProcessAdmin)
