from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from unittest.mock import patch

User = get_user_model()

class LoginTests(TestCase):
    """Test the user login API with thorough test cases."""

    def setUp(self):
        self.client = APIClient()
        self.login_url = '/api/v1/users/login/'
        # Create a test user for login tests
        self.test_user = User.objects.create_user(
            email='testuser@example.com',
            password='testpassword123',
            full_name='Test User'
        )

    def test_login_successful(self):
        """Test successful login with valid credentials."""
        payload = {
            'email': 'testuser@example.com',
            'password': 'testpassword123'
        }
        response = self.client.post(self.login_url, payload)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
        self.assertIn('user', response.data)
        self.assertEqual(response.data['user']['email'], 'testuser@example.com')
        self.assertEqual(response.data['user']['full_name'], 'Test User')

    def test_login_incorrect_password(self):
        """Test login fails with incorrect password."""
        payload = {
            'email': 'testuser@example.com',
            'password': 'wrongpassword123'
        }
        response = self.client.post(self.login_url, payload)
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn('detail', response.data)
        self.assertEqual(response.data['detail'], 'Invalid credentials')

    def test_login_nonexistent_user(self):
        """Test login fails with non-existent email."""
        payload = {
            'email': 'nonexistent@example.com',
            'password': 'testpassword123'
        }
        response = self.client.post(self.login_url, payload)
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn('detail', response.data)
        self.assertEqual(response.data['detail'], 'Invalid credentials')

    def test_login_missing_fields(self):
        """Test login fails with missing fields."""
        # Missing email
        payload = {
            'password': 'testpassword123'
        }
        response = self.client.post(self.login_url, payload)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
        # Missing password
        payload = {
            'email': 'testuser@example.com'
        }
        response = self.client.post(self.login_url, payload)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    @patch('users.views.LoginRateThrottle.allow_request')
    def test_login_rate_limiting(self, mock_allow_request):
        """Test rate limiting on the login endpoint."""
        # Set up the mock to simulate rate limit exceeded
        mock_allow_request.return_value = False
        
        payload = {
            'email': 'testuser@example.com',
            'password': 'testpassword123'
        }
        response = self.client.post(self.login_url, payload)
        
        self.assertEqual(response.status_code, status.HTTP_429_TOO_MANY_REQUESTS)
        mock_allow_request.assert_called_once()
