from django.contrib.auth.models import User
from rest_framework.test import APITestCase


class AccountTests(APITestCase):
    def test_register_user_hashes_password(self):
        response = self.client.post('/api/auth/register/', {
            'username': 'customer',
            'email': 'customer@example.com',
            'password': 'pass12345',
        }, format='json')
        self.assertEqual(response.status_code, 201)
        user = User.objects.get(username='customer')
        self.assertTrue(user.check_password('pass12345'))

    def test_demo_social_login_returns_jwt(self):
        response = self.client.post('/api/auth/social-login/', {
            'provider': 'google',
            'access_token': 'demo-token',
            'email': 'oauth@example.com',
            'username': 'oauth_user',
        }, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertIn('access', response.data)
        self.assertEqual(response.data['user']['username'], 'oauth_user')
