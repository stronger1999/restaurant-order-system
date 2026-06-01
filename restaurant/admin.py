from django.contrib import admin
from .models import RestaurantTable, MenuCategory, MenuItem
admin.site.register(RestaurantTable)
admin.site.register(MenuCategory)
admin.site.register(MenuItem)
