from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

from django.conf import settings
from django.conf.urls.static import static

from restaurant.views import RestaurantTableViewSet, MenuCategoryViewSet, MenuItemViewSet
from orders.views import OrderViewSet
from payments.views import PaymentViewSet

router = DefaultRouter()

router.register('tables', RestaurantTableViewSet)
router.register('categories', MenuCategoryViewSet)
router.register('menu-items', MenuItemViewSet)
router.register('orders', OrderViewSet, basename='orders')
router.register('payments', PaymentViewSet, basename='payments')

urlpatterns = [

    path('', include('frontend.urls')),

    path('admin/', admin.site.urls),

    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),

    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),

    path('api/auth/', include('accounts.urls')),

    path('api/', include(router.urls)),

]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )