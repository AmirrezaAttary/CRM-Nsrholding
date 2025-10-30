from django.urls import path,include
from django.conf import settings
from app.crm.api.v1.views import CallReportViewSet, CargoAnnouncementViewSet, PurchaseProcessViewSet, SaleReportViewSet, SaleReportExportView, SaleReportBulkExportView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('call-reports', CallReportViewSet, basename='callreport')
router.register('cargo-announcements', CargoAnnouncementViewSet, basename='cargoannouncement')
router.register('purchase-process', PurchaseProcessViewSet, basename='purchase-process')
router.register('sale-reports', SaleReportViewSet, basename='sale-reports')

urlpatterns = [
    path('sale-reports/<int:pk>/export/', SaleReportExportView.as_view(), name='sale-report-export'),
    path('sale-reports/export/', SaleReportBulkExportView.as_view(), name='sale-report-export-list'),
]

urlpatterns += router.urls