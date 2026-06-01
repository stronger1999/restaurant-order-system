from rest_framework import serializers
from restaurant.models import MenuItem
from .models import Order, OrderItem

class OrderItemSerializer(serializers.ModelSerializer):
    line_total = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    class Meta: model = OrderItem; fields = ['id','menu_item','quantity','unit_price','line_total']; read_only_fields=['unit_price']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    total_amount = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    class Meta:
        model = Order
        fields = ['id','customer','table','status','notes','items','total_amount','created_at','updated_at']
        read_only_fields = ['customer','status','created_at','updated_at']

class AddOrderItemSerializer(serializers.Serializer):
    menu_item_id = serializers.IntegerField()
    quantity = serializers.IntegerField(min_value=1)
    def validate_menu_item_id(self, value):
        if not MenuItem.objects.filter(id=value, is_available=True).exists():
            raise serializers.ValidationError('Menu item not found or unavailable.')
        return value
