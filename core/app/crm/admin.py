from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.db.models import Q
from .models import CallReport, FieldActivity, ValidationLevel
from django_jalali.admin.filters import JDateFieldListFilter
from django_jalali.admin.widgets import AdminjDateWidget

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

admin.site.register(FieldActivity, FieldActivityAdmin)
admin.site.register(CallReport, CallReportAdmin)
admin.site.register(ValidationLevel,ValidationLevelAdmin)