from django.contrib import admin, messages
from .models import Payment


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'method', 'status', 'amount', 'approved_by', 'created_at')
    list_filter = ('method', 'status', 'created_at')
    search_fields = ('order__id', 'transaction_reference', 'order__customer__username')
    readonly_fields = ('created_at', 'updated_at', 'transaction_reference', 'failure_reason')
    actions = ['approve_offline_payments', 'reject_offline_payments']

    @admin.action(description='Approve selected offline payments')
    def approve_offline_payments(self, request, queryset):
        updated = queryset.filter(method=Payment.Method.OFFLINE, status=Payment.Status.PENDING).update(
            status=Payment.Status.APPROVED, approved_by=request.user
        )
        self.message_user(request, f'{updated} offline payment(s) approved.', messages.SUCCESS)

    @admin.action(description='Reject selected offline payments')
    def reject_offline_payments(self, request, queryset):
        updated = queryset.filter(method=Payment.Method.OFFLINE, status=Payment.Status.PENDING).update(
            status=Payment.Status.REJECTED, approved_by=request.user
        )
        self.message_user(request, f'{updated} offline payment(s) rejected.', messages.WARNING)
