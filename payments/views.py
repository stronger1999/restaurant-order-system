from rest_framework import viewsets, permissions, decorators, response
from orders.models import Order
from .models import Payment
from .serializers import PaymentSerializer, OnlinePaymentSerializer, OfflinePaymentSerializer
from .services import process_sandbox_online_payment
from .tasks import send_payment_notification

class PaymentViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticated]
    def get_queryset(self):
        qs = Payment.objects.select_related('order','approved_by').all().order_by('-created_at')
        return qs if self.request.user.is_staff else qs.filter(order__customer=self.request.user)
    @decorators.action(detail=False, methods=['post'])
    def online(self, request):
        s = OnlinePaymentSerializer(data=request.data); s.is_valid(raise_exception=True)
        order = Order.objects.get(id=s.validated_data['order_id'])
        if not request.user.is_staff and order.customer != request.user:
            return response.Response({'detail':'Not allowed.'}, status=403)
        payment = Payment.objects.create(order=order, method=Payment.Method.ONLINE, amount=order.total_amount)
        payment = process_sandbox_online_payment(payment, s.validated_data['sandbox_token'])
        send_payment_notification.delay(payment.id, payment.status)
        return response.Response(PaymentSerializer(payment).data)
    @decorators.action(detail=False, methods=['post'])
    def offline(self, request):
        s = OfflinePaymentSerializer(data=request.data); s.is_valid(raise_exception=True)
        order = Order.objects.get(id=s.validated_data['order_id'])
        if not request.user.is_staff and order.customer != request.user:
            return response.Response({'detail':'Not allowed.'}, status=403)
        payment = Payment.objects.create(order=order, method=Payment.Method.OFFLINE, status=Payment.Status.PENDING, amount=order.total_amount)
        return response.Response(PaymentSerializer(payment).data)
    @decorators.action(detail=True, methods=['post'], permission_classes=[permissions.IsAdminUser])
    def approve_offline(self, request, pk=None):
        payment = self.get_object()
        if payment.method != Payment.Method.OFFLINE:
            return response.Response({'detail':'Only offline payments can be approved manually.'}, status=400)
        payment.status = Payment.Status.APPROVED; payment.approved_by = request.user; payment.save()
        send_payment_notification.delay(payment.id, payment.status)
        return response.Response(PaymentSerializer(payment).data)
    @decorators.action(detail=True, methods=['post'], permission_classes=[permissions.IsAdminUser])
    def reject_offline(self, request, pk=None):
        payment = self.get_object(); payment.status = Payment.Status.REJECTED; payment.approved_by = request.user; payment.save()
        send_payment_notification.delay(payment.id, payment.status)
        return response.Response(PaymentSerializer(payment).data)
