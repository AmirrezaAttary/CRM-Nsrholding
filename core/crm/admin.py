from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.db.models import Q
from .models import Customer, Lead, Interaction, Opportunity, Task, Document, Tag


# ---------- Inlines ----------
class InteractionInline(admin.TabularInline):
    model = Interaction
    extra = 0
    fields = ("type", "subject", "interaction_date", "created_by")
    autocomplete_fields = ("created_by",)
    show_change_link = True

class TaskInline(admin.TabularInline):
    model = Task
    extra = 0
    fields = ("title", "due_date", "status", "assigned_to", "related_opportunity")
    autocomplete_fields = ("assigned_to", "related_opportunity")
    show_change_link = True

class DocumentInline(admin.TabularInline):
    model = Document
    extra = 0
    fields = ("title", "file", "uploaded_at")
    readonly_fields = ("uploaded_at",)
    show_change_link = True


# ---------- فیلتر سفارشی نمونه ----------
class HasEmailFilter(admin.SimpleListFilter):
    title = _("ایمیل دارد؟")
    parameter_name = "has_email"

    def lookups(self, request, model_admin):
        return (("yes", _("بله")), ("no", _("خیر")))

    def queryset(self, request, queryset):
        if self.value() == "yes":
            return queryset.filter(~Q(email=None)).exclude(email__exact="")
        if self.value() == "no":
            return queryset.filter(Q(email=None) | Q(email__exact=""))
        return queryset


# ---------- Customer ----------
@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ("phone_number", "full_name", "company", "city", "created_by", "created_at")
    list_display_links = ("phone_number", "full_name")
    search_fields = ("phone_number", "first_name", "last_name", "company", "city")
    list_filter = (HasEmailFilter, "city", "created_by")
    readonly_fields = ("created_at", "updated_at")
    inlines = (InteractionInline, TaskInline, DocumentInline)
    autocomplete_fields = ("created_by",)
    ordering = ("-id",)
    date_hierarchy = "created_at"
    filter_horizontal = ("tags",) if hasattr(Customer, "tags") else ()

    def full_name(self, obj):
        return f"{obj.first_name or ''} {obj.last_name or ''}".strip()
    full_name.short_description = _("نام کامل")

    def save_model(self, request, obj, form, change):
        if not obj.created_by_id:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)


# ---------- Lead ----------
@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = ("phone_number", "name", "source", "status", "assigned_to", "created_at")
    list_filter = ("source", "status", "assigned_to")
    search_fields = ("phone_number", "name")
    autocomplete_fields = ("assigned_to",)
    ordering = ("-id",)
    date_hierarchy = "created_at"


# ---------- Interaction ----------
@admin.register(Interaction)
class InteractionAdmin(admin.ModelAdmin):
    list_display = ("customer", "type", "subject", "interaction_date", "created_by")
    list_filter = ("type", "created_by")
    search_fields = ("customer__phone_number", "subject", "description")
    autocomplete_fields = ("customer", "created_by")
    ordering = ("-interaction_date",)


# ---------- Opportunity ----------
@admin.register(Opportunity)
class OpportunityAdmin(admin.ModelAdmin):
    list_display = ("title", "customer_phone", "stage", "value", "expected_close_date", "created_at")
    list_filter = ("stage",)
    search_fields = ("title", "customer__phone_number")
    autocomplete_fields = ("customer",)
    ordering = ("-id",)
    date_hierarchy = "created_at"

    @admin.display(description=_("شماره مشتری"))
    def customer_phone(self, obj):
        return obj.customer.phone_number


# ---------- Task ----------
@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("title", "status", "due_date", "assigned_to", "customer_phone", "opportunity_title", "created_at")
    list_filter = ("status", "assigned_to")
    search_fields = ("title", "related_customer__phone_number", "related_opportunity__title")
    autocomplete_fields = ("assigned_to", "related_customer", "related_opportunity")
    ordering = ("-due_date",)
    date_hierarchy = "created_at"

    @admin.display(description=_("شماره مشتری"))
    def customer_phone(self, obj):
        return obj.related_customer.phone_number if obj.related_customer else "-"

    @admin.display(description=_("فرصت"))
    def opportunity_title(self, obj):
        return obj.related_opportunity.title if obj.related_opportunity else "-"


# ---------- Document ----------
@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ("title", "customer", "uploaded_at")
    search_fields = ("title", "customer__phone_number")
    autocomplete_fields = ("customer",)
    readonly_fields = ("uploaded_at",)
    ordering = ("-uploaded_at",)


# ---------- Tag ----------
@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("name", "customers_count")
    search_fields = ("name",)
    filter_horizontal = ("customers",)
    ordering = ("name",)

    @admin.display(description=_("تعداد مشتریان"))
    def customers_count(self, obj):
        return obj.customers.count()
