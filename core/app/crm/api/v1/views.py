from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404

from app.crm.models import CallReport, CargoAnnouncement, PurchaseProcess, SaleReport
from app.crm.api.v1.filters import CallReportFilter, SaleReportFilter
from app.crm.api.v1.serializer import (
    CallReportSerializer, 
    CargoAnnouncementSerializer, 
    PurchaseProcessSerializer, 
    SaleReportSerializer
)
from app.crm.api.v1.paginations import CustomPagination

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response



class CallReportViewSet(viewsets.ModelViewSet):
   
    queryset = CallReport.objects.all().order_by('-created_at')
    serializer_class = CallReportSerializer

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = CallReportFilter  
    search_fields = ['name', 'number', 'province', 'city']
    ordering_fields = ['created_at', 'name']

    # Add custom pagination
    pagination_class = CustomPagination

    @action(detail=True, methods=['get'], url_path='go-to-purchase')
    def go_to_purchase(self, request, pk=None):
        call_report = self.get_object()
        purchase_process, created = PurchaseProcess.objects.get_or_create(call_report=call_report)
        purchase_url = f"/crm/api/v1/purchase-process/{purchase_process.id}/"
        return redirect(purchase_url)

class CargoAnnouncementViewSet(viewsets.ModelViewSet):
    queryset = CargoAnnouncement.objects.all()
    serializer_class = CargoAnnouncementSerializer

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]

    
    filterset_fields = ['load_type', 'product_type__id', 'country_name__name']
    search_fields = ['product_type__name', 'country_name__name']
    ordering_fields = ['product_price', 'id']

    # Add custom pagination
    pagination_class = CustomPagination

class PurchaseProcessViewSet(viewsets.ModelViewSet):
    queryset = PurchaseProcess.objects.all().order_by('-created_at')
    serializer_class = PurchaseProcessSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['load_type', 'market_place_type']
    search_fields = ['call_report__name', 'call_report__number', 'buyer_name']
    ordering_fields = ['created_at', 'buyer_name', 'call_report__name']
    pagination_class = CustomPagination

    @action(detail=True, methods=['get'], url_path='go-to-sale-report')
    def go_to_sale_report(self, request, pk=None):
        purchase_process = self.get_object()

        sale_type_value = getattr(purchase_process, 'load_type', None) or 'market_place'

        sale_report, created = SaleReport.objects.get_or_create(
            purchase_process=purchase_process,
            defaults={'sale_type': sale_type_value}
        )

        if not created and sale_report.sale_type != sale_type_value:
            sale_report.sale_type = sale_type_value
            sale_report.save(update_fields=['sale_type'])

        sale_report_url = f"/crm/api/v1/sale-reports/{sale_report.id}/"
        return redirect(sale_report_url)
    
    
#########################################################################

class SaleReportViewSet(viewsets.ModelViewSet):
    queryset = SaleReport.objects.all()
    serializer_class = SaleReportSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = SaleReportFilter
    pagination_class = CustomPagination

    