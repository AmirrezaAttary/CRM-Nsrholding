from django_filters.rest_framework import DjangoFilterBackend, FilterSet, ChoiceFilter
import django_filters
from app.crm.models import CallReport, SaleReport

class CallReportFilter(FilterSet):
    
    validation = ChoiceFilter(
        field_name='validation__name', 
        choices=[('خوب','خوب'), ('متوسط','متوسط'), ('بد','بد')]
    )

    class Meta:
        model = CallReport
        fields = ['validation']

class SaleReportFilter(django_filters.FilterSet):
    
    SALE_TYPE_CHOICES = [
        ('market_place', 'بازارگاهی'),
        ('market_outside', 'خارج بازارگاهی'),
        ('quota', 'سهمیه'),
        ('overhead', 'روبار'),
    ]

    sale_type = django_filters.ChoiceFilter(
        field_name='sale_type',
        choices=SALE_TYPE_CHOICES,
        label='نوع خرید (Sale Type)'
    )

    class Meta:
        model = SaleReport
        fields = ['sale_type']