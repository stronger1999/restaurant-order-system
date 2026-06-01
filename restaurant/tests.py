from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from restaurant.models import MenuCategory, MenuItem


class RestaurantPermissionTests(APITestCase):
    def setUp(self):
        self.category = MenuCategory.objects.create(name='Pizza')
        self.item = MenuItem.objects.create(category=self.category, name='Margherita', price='20.00')
        self.customer = User.objects.create_user(username='customer', password='pass12345')
        self.admin = User.objects.create_superuser(username='admin', password='pass12345')

    def test_public_can_read_menu_items(self):
        response = self.client.get('/api/menu-items/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    def test_customer_cannot_create_menu_item(self):
        self.client.force_authenticate(self.customer)
        response = self.client.post('/api/menu-items/', {
            'category': self.category.id,
            'name': 'Pepperoni',
            'price': '25.00',
            'is_available': True,
        }, format='json')
        self.assertEqual(response.status_code, 403)

    def test_admin_can_create_menu_item(self):
        self.client.force_authenticate(self.admin)
        response = self.client.post('/api/menu-items/', {
            'category': self.category.id,
            'name': 'Pepperoni',
            'price': '25.00',
            'is_available': True,
        }, format='json')
        self.assertEqual(response.status_code, 201)
