from rest_framework import serializers
from orders.models import Order
from .models import Payment

class PaymentSerializer(serializers.ModelSerializer):
    class Meta: model = Payment; fields = '__all__'; read_only_fields = ['status','amount','transaction_reference','failure_reason','approved_by']

class OnlinePaymentSerializer(serializers.Serializer):
    order_id = serializers.IntegerField()
    sandbox_token = serializers.CharField(help_text='Use tok_success or tok_fail')
    def validate_order_id(self, value):
        if not Order.objects.filter(id=value).exists(): raise serializers.ValidationError('Order not found.')
        return value

class OfflinePaymentSerializer(serializers.Serializer):
    order_id = serializers.IntegerField()
    note = serializers.CharField(required=False, allow_blank=True)
