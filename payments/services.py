import uuid
from decimal import Decimal
from django.conf import settings
from .models import Payment


def _approve_demo_payment(payment):
    payment.status = Payment.Status.APPROVED
    payment.transaction_reference = f"SANDBOX-{uuid.uuid4().hex[:12].upper()}"
    payment.failure_reason = ''
    payment.save(update_fields=['status', 'failure_reason', 'transaction_reference', 'updated_at'])
    return payment


def _fail_demo_payment(payment, reason='Sandbox payment failed: declined test card.'):
    payment.status = Payment.Status.FAILED
    payment.failure_reason = reason
    payment.transaction_reference = ''
    payment.save(update_fields=['status', 'failure_reason', 'transaction_reference', 'updated_at'])
    return payment


def process_sandbox_online_payment(payment, sandbox_token):
    """Process online payment in a way suitable for university sandbox testing.

    Supported modes:
    - Demo mode: deterministic tokens without external credentials.
      tok_success -> APPROVED, tok_fail -> FAILED.
    - Stripe mode: when STRIPE_DEMO_MODE=False and STRIPE_SECRET_KEY exists,
      create a Stripe PaymentIntent in sandbox mode.
    """
    if sandbox_token in {'tok_fail', 'pm_card_chargeDeclined', '4000000000000002'}:
        return _fail_demo_payment(payment, 'Sandbox payment failed: card declined / insufficient funds.')

    if getattr(settings, 'STRIPE_DEMO_MODE', True) or not getattr(settings, 'STRIPE_SECRET_KEY', ''):
        return _approve_demo_payment(payment)

    try:
        import stripe
        stripe.api_key = settings.STRIPE_SECRET_KEY
        amount_minor = int(Decimal(payment.amount) * 100)
        intent = stripe.PaymentIntent.create(
            amount=amount_minor,
            currency=getattr(settings, 'STRIPE_CURRENCY', 'pln'),
            payment_method=sandbox_token,
            confirm=True,
            automatic_payment_methods={'enabled': True, 'allow_redirects': 'never'},
            metadata={'order_id': str(payment.order_id), 'payment_id': str(payment.id)},
        )
        if intent.status in {'succeeded', 'requires_capture'}:
            payment.status = Payment.Status.APPROVED
            payment.transaction_reference = intent.id
            payment.failure_reason = ''
        else:
            payment.status = Payment.Status.FAILED
            payment.failure_reason = f'Stripe sandbox returned status: {intent.status}'
        payment.save(update_fields=['status', 'failure_reason', 'transaction_reference', 'updated_at'])
        return payment
    except Exception as exc:
        return _fail_demo_payment(payment, f'Stripe sandbox error: {exc}')
