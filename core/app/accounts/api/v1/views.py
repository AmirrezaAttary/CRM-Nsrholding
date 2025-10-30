from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import generics, status
from rest_framework.response import Response
from app.accounts.models import User
from app.accounts.api.v1.serializers import UserSerializer, RegisterSerializer
from rest_framework.permissions import AllowAny
from app.crm.api.v1.paginations import CustomPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from app.accounts.api.v1.filters import UserFilter



class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    # Add custom pagination
    pagination_class = CustomPagination
    
    filterset_class = UserFilter
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['type', 'is_active', 'is_verified']
    search_fields = ['first_name', 'last_name', 'phone_number']
    ordering_fields = ['created_date', 'updated_date']
    ordering = ['-created_date']
    
    

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]
   
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(
            {"message": "ثبت‌نام با موفقیت انجام شد"},
            status=status.HTTP_201_CREATED
        )

    
