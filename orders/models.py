from decimal import Decimal
from django.conf import settings
from django.db import models
from restaurant.models import RestaurantTable, MenuItem

class Order(models.Model):
    class Status(models.TextChoices):
        DRAFT='DRAFT','Draft'; SUBMITTED='SUBMITTED','Submitted'; PREPARING='PREPARING','Preparing'; READY='READY','Ready'; CANCELLED='CANCELLED','Cancelled'
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL, related_name='orders')
    table = models.ForeignKey(RestaurantTable, null=True, blank=True, on_delete=models.SET_NULL)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.DRAFT)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    @property
    def total_amount(self):
        return sum((item.line_total for item in self.items.all()), Decimal('0.00'))
    def __str__(self): return f"Order #{self.id} - {self.status}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    menu_item = models.ForeignKey(MenuItem, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField(default=1)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    @property
    def line_total(self): return self.unit_price * self.quantity
    def save(self, *args, **kwargs):
        if not self.unit_price: self.unit_price = self.menu_item.price
        super().save(*args, **kwargs)
