from rest_framework import viewsets, permissions
from .models import RestaurantTable, MenuCategory, MenuItem
from .serializers import RestaurantTableSerializer, MenuCategorySerializer, MenuItemSerializer

class StaffWritePermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS: return True
        return request.user and request.user.is_staff

class RestaurantTableViewSet(viewsets.ModelViewSet):
    queryset = RestaurantTable.objects.all().order_by('number')
    serializer_class = RestaurantTableSerializer
    permission_classes = [StaffWritePermission]

class MenuCategoryViewSet(viewsets.ModelViewSet):
    queryset = MenuCategory.objects.all().order_by('name')
    serializer_class = MenuCategorySerializer
    permission_classes = [StaffWritePermission]

class MenuItemViewSet(viewsets.ModelViewSet):
    queryset = MenuItem.objects.select_related('category').all().order_by('name')
    serializer_class = MenuItemSerializer
    filterset_fields = ['category','is_available']
    permission_classes = [StaffWritePermission]
