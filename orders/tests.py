from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from restaurant.models import MenuCategory, MenuItem, RestaurantTable
from orders.models import Order, OrderItem

class OrderTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='u1', password='pass12345')
        self.client.force_authenticate(self.user)
        self.table = RestaurantTable.objects.create(number=1)
        self.cat = MenuCategory.objects.create(name='Pizza')
        self.item = MenuItem.objects.create(category=self.cat, name='Margherita', price='20.00')
    def test_create_order_and_add_item(self):
        r = self.client.post('/api/orders/', {'table': self.table.id, 'notes':'test'}, format='json')
        self.assertEqual(r.status_code, 201)
        order_id = r.data['id']
        r = self.client.post(f'/api/orders/{order_id}/add_item/', {'menu_item_id': self.item.id, 'quantity':2}, format='json')
        self.assertEqual(r.status_code, 200)
        self.assertEqual(str(Order.objects.get(id=order_id).total_amount), '40.00')
    def test_submit_order(self):
        order = Order.objects.create(customer=self.user, table=self.table)
        OrderItem.objects.create(order=order, menu_item=self.item, quantity=1, unit_price=self.item.price)
        r = self.client.post(f'/api/orders/{order.id}/submit/')
        self.assertEqual(r.status_code, 200)
        order.refresh_from_db()
        self.assertEqual(order.status, Order.Status.SUBMITTED)
