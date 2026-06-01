from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static

from rest_framework.routers import DefaultRouter
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

from restaurant.views import (
    RestaurantTableViewSet,
    MenuCategoryViewSet,
    MenuItemViewSet,
)
from orders.views import OrderViewSet
from payments.views import PaymentViewSet


router = DefaultRouter()
router.register('tables', RestaurantTableViewSet, basename='tables')
router.register('categories', MenuCategoryViewSet, basename='categories')
router.register('menu-items', MenuItemViewSet, basename='menu-items')
router.register('orders', OrderViewSet, basename='orders')
router.register('payments', PaymentViewSet, basename='payments')


urlpatterns = [
    # Frontend
    path('', include('frontend.urls')),

    # Google OAuth2
    path('', include('social_django.urls', namespace='social')),

    # Admin
    path('secure-admin-2026/', admin.site.urls),

    # Swagger / OpenAPI
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),

    # API Auth
    path('api/auth/', include('accounts.urls')),

    # API Router
    path('api/', include(router.urls)),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)