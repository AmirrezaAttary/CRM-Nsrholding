from django.urls import path, include
from django.conf import settings

urlpatterns = [
    path('v1/', include('app.accounts.api.v1.urls')),
]
