from django.urls import path,include
from django.conf import settings
from app.crm.api.v1.views import (CallReportViewSet, CargoAnnouncementViewSet, PurchaseProcessViewSet, 
                                  SaleReportViewSet, SaleReportExportView, SaleReportBulkExportView,
                                  ProductTypeViewSet, CountryNameViewSet, PortNameViewSet,
                                  LoadingTimeViewSet, TransactionTypeViewSet,FieldActivityViewSet,
                                  ValidationLevelViewSet,SupplyStatusViewSet)
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('call-reports', CallReportViewSet, basename='callreport')
router.register('cargo-announcements', CargoAnnouncementViewSet, basename='cargoannouncement')
router.register('purchase-process', PurchaseProcessViewSet, basename='purchase-process')
router.register('sale-reports', SaleReportViewSet, basename='sale-reports')
router.register("product-types", ProductTypeViewSet)
router.register("countries", CountryNameViewSet)
router.register("ports", PortNameViewSet)
router.register("loading-times", LoadingTimeViewSet)
router.register("transaction-types", TransactionTypeViewSet)
router.register("field-activity", FieldActivityViewSet)
router.register("validation-level", ValidationLevelViewSet)
router.register("supply-status", SupplyStatusViewSet)

urlpatterns = [
    path('sale-reports/<int:pk>/export/', SaleReportExportView.as_view(), name='sale-report-export'),
    path('sale-reports/export/', SaleReportBulkExportView.as_view(), name='sale-report-export-list'),
]

urlpatterns += router.urls