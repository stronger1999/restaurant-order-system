from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from restaurant.models import MenuCategory, MenuItem, RestaurantTable
from orders.models import Order, OrderItem
from payments.models import Payment

class PaymentTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='u1', password='pass12345')
        self.admin = User.objects.create_superuser(username='admin', password='pass12345')
        self.client.force_authenticate(self.user)
        table = RestaurantTable.objects.create(number=1)
        cat = MenuCategory.objects.create(name='Drinks')
        item = MenuItem.objects.create(category=cat, name='Water', price='5.00')
        self.order = Order.objects.create(customer=self.user, table=table)
        OrderItem.objects.create(order=self.order, menu_item=item, quantity=2, unit_price=item.price)
    def test_online_payment_failure(self):
        r = self.client.post('/api/payments/online/', {'order_id': self.order.id, 'sandbox_token':'tok_fail'}, format='json')
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.data['status'], Payment.Status.FAILED)
    def test_offline_approval(self):
        r = self.client.post('/api/payments/offline/', {'order_id': self.order.id}, format='json')
        payment_id = r.data['id']
        self.client.force_authenticate(self.admin)
        r = self.client.post(f'/api/payments/{payment_id}/approve_offline/')
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.data['status'], Payment.Status.APPROVED)
