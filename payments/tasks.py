from celery import shared_task
import time
import random

from payments.models import Payment


@shared_task
def send_payment_notification(payment_id, status=None):
    payment = Payment.objects.get(id=payment_id)

    if status is None:
        status = payment.status

    print(f'[ASYNC] Payment {payment.id} changed to {status}')


@shared_task
def process_blik_payment(payment_id, blik_code):
    time.sleep(5)

    SUCCESS_CODES = ['111111', '222222', '333333']
    FAILED_CODES = ['999999', '888888', '777777']

    payment = Payment.objects.get(id=payment_id)

    if blik_code in SUCCESS_CODES:
        payment.status = 'APPROVED'
        payment.failure_reason = ''

    elif blik_code in FAILED_CODES:
        payment.status = 'FAILED'
        payment.failure_reason = 'Sandbox rejected BLIK payment'

    else:
        payment.status = 'FAILED' if random.random() < 0.3 else 'APPROVED'
        payment.failure_reason = (
            'BLIK payment rejected or not confirmed'
            if payment.status == 'FAILED'
            else ''
        )

    payment.save()

    print(f'[ASYNC] BLIK payment {payment.id} ({blik_code}) changed to {payment.status}')

    send_payment_notification.delay(payment.id, payment.status)