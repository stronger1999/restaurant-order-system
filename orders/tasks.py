from celery import shared_task

@shared_task
def send_order_status_notification(order_id, status):
    print(f"[ASYNC] Notification: Order {order_id} status changed to {status}")
    return True
