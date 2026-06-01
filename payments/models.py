from django.conf import settings
from django.db import models
from orders.models import Order

class Payment(models.Model):
    class Method(models.TextChoices): ONLINE='ONLINE','Online'; OFFLINE='OFFLINE','Offline'
    class Status(models.TextChoices): PENDING='PENDING','Pending'; APPROVED='APPROVED','Approved'; FAILED='FAILED','Failed'; REJECTED='REJECTED','Rejected'
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='payments')
    method = models.CharField(max_length=20, choices=Method.choices)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_reference = models.CharField(max_length=120, blank=True)
    failure_reason = models.TextField(blank=True)
    approved_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
