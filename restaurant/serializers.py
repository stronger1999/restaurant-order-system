from rest_framework import serializers
from .models import RestaurantTable, MenuCategory, MenuItem
class RestaurantTableSerializer(serializers.ModelSerializer):
    class Meta: model = RestaurantTable; fields = '__all__'
class MenuCategorySerializer(serializers.ModelSerializer):
    class Meta: model = MenuCategory; fields = '__all__'
class MenuItemSerializer(serializers.ModelSerializer):
    class Meta: model = MenuItem; fields = '__all__'
