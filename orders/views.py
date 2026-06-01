from rest_framework import viewsets, permissions, decorators, response, status
from restaurant.models import MenuItem
from .models import Order, OrderItem
from .serializers import OrderSerializer, AddOrderItemSerializer
from .tasks import send_order_status_notification

class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]
    def get_queryset(self):
        qs = Order.objects.prefetch_related('items__menu_item').all().order_by('-created_at')
        return qs if self.request.user.is_staff else qs.filter(customer=self.request.user)
    def perform_create(self, serializer):
        serializer.save(customer=self.request.user)
    @decorators.action(detail=True, methods=['post'])
    def add_item(self, request, pk=None):
        order = self.get_object()
        if order.status != Order.Status.DRAFT:
            return response.Response({'detail':'Items can only be added to draft orders.'}, status=400)
        s = AddOrderItemSerializer(data=request.data); s.is_valid(raise_exception=True)
        item = MenuItem.objects.get(id=s.validated_data['menu_item_id'])
        OrderItem.objects.create(order=order, menu_item=item, quantity=s.validated_data['quantity'], unit_price=item.price)
        return response.Response(OrderSerializer(order).data)
    def _set_status(self, order, new_status):
        order.status = new_status; order.save(update_fields=['status','updated_at'])
        send_order_status_notification.delay(order.id, new_status)
        return response.Response(OrderSerializer(order).data)
    @decorators.action(detail=True, methods=['post'])
    def submit(self, request, pk=None): return self._set_status(self.get_object(), Order.Status.SUBMITTED)
    @decorators.action(detail=True, methods=['post'], permission_classes=[permissions.IsAdminUser])
    def mark_preparing(self, request, pk=None): return self._set_status(self.get_object(), Order.Status.PREPARING)
    @decorators.action(detail=True, methods=['post'], permission_classes=[permissions.IsAdminUser])
    def mark_ready(self, request, pk=None): return self._set_status(self.get_object(), Order.Status.READY)
    @decorators.action(detail=True, methods=['post'])
    def cancel(self, request, pk=None): return self._set_status(self.get_object(), Order.Status.CANCELLED)
