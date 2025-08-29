from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
import json

User = get_user_model()


class UserModelTests(TestCase):
    """Test the User model."""

    def test_create_user_with_email_successful(self):
        """Test creating a new user with an email is successful."""
        email = 'test@example.com'
        password = 'testpass123'
        full_name = 'Test User'
        user = User.objects.create_user(
            email=email,
            password=password,
            full_name=full_name
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))
        self.assertEqual(user.full_name, full_name)

    def test_create_superuser(self):
        """Test creating a new superuser."""
        email = 'admin@example.com'
        password = 'testpass123'
        full_name = 'Admin User'
        user = User.objects.create_superuser(
            email=email,
            password=password,
            full_name=full_name
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)


class UserAPITests(TestCase):
    """Test the user API."""

    def setUp(self):
        self.client = APIClient()
        self.register_url = '/api/v1/users/register/'
        self.login_url = '/api/v1/users/login/'
        self.password_reset_request_url = '/api/v1/users/password-reset/'
        self.password_reset_confirm_url = '/api/v1/users/password-reset/confirm/'
        self.profile_url = '/api/v1/users/profile/'
        
        # Create a test user for login and password reset tests
        self.user = User.objects.create_user(
            email='existing@example.com',
            password='existingpass123',
            full_name='Existing User'
        )

    def test_create_user_successful(self):
        """Test creating user is successful."""
        payload = {
            'email': 'test@example.com',
            'password': 'testpass123',
            'password_confirm': 'testpass123',
            'full_name': 'Test User',
        }
        res = self.client.post(self.register_url, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = User.objects.get(email=payload['email'])
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data)
        
        # Verify JWT tokens are returned
        self.assertIn('access', res.data)
        self.assertIn('refresh', res.data)
        
    def test_create_user_invalid_payload(self):
        """Test creating user with invalid payload fails."""
        # Test with invalid email
        payload = {
            'email': 'invalidemail',
            'password': 'testpass123',
            'password_confirm': 'testpass123',
            'full_name': 'Test User',
        }
        res = self.client.post(self.register_url, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        
        # Test with password mismatch
        payload = {
            'email': 'test@example.com',
            'password': 'testpass123',
            'password_confirm': 'differentpass',
            'full_name': 'Test User',
        }
        res = self.client.post(self.register_url, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        
        # Test with missing fields
        payload = {
            'email': 'test@example.com',
            'password': 'testpass123',
        }
        res = self.client.post(self.register_url, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_user_login_successful(self):
        """Test user login with valid credentials."""
        payload = {
            'email': 'existing@example.com',
            'password': 'existingpass123'
        }
        res = self.client.post(self.login_url, payload)
        
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn('access', res.data)
        self.assertIn('refresh', res.data)
        self.assertIn('user', res.data)
        
    def test_user_login_invalid_credentials(self):
        """Test user login with invalid credentials fails."""
        # Wrong password
        payload = {
            'email': 'existing@example.com',
            'password': 'wrongpassword'
        }
        res = self.client.post(self.login_url, payload)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
        
        # Wrong email
        payload = {
            'email': 'nonexistent@example.com',
            'password': 'existingpass123'
        }
        res = self.client.post(self.login_url, payload)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
        
    def test_password_reset_request(self):
        """Test requesting a password reset token."""
        # Valid email
        payload = {
            'email': 'existing@example.com'
        }
        res = self.client.post(self.password_reset_request_url, payload)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn('detail', res.data)
        # In a real test, we would also check that a token was generated
        # but since we're using a mock Redis here, we'll skip that part
        
        # Non-existent email (should still return 200 for security reasons)
        payload = {
            'email': 'nonexistent@example.com'
        }
        res = self.client.post(self.password_reset_request_url, payload)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        
    def test_password_reset_confirm(self):
        """Test confirming a password reset with token."""
        # This test is a bit tricky since we need a valid token
        # In a real test environment, we would mock the token generation and validation
        # For now, we'll just test the error case
        payload = {
            'token': 'invalid_token',
            'new_password': 'newpassword123',
            'new_password_confirm': 'newpassword123'
        }
        res = self.client.post(self.password_reset_confirm_url, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        
        # Password mismatch
        payload = {
            'token': 'some_token',
            'new_password': 'newpassword123',
            'new_password_confirm': 'differentpassword'
        }
        res = self.client.post(self.password_reset_confirm_url, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_access_profile_with_token(self):
        """Test accessing profile with valid token."""
        # Login to get token
        login_payload = {
            'email': 'existing@example.com',
            'password': 'existingpass123'
        }
        login_res = self.client.post(self.login_url, login_payload)
        self.assertEqual(login_res.status_code, status.HTTP_200_OK)
        
        # Access profile with token
        token = login_res.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        res = self.client.get(self.profile_url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['email'], 'existing@example.com')
        self.assertEqual(res.data['full_name'], 'Existing User')
        
    def test_access_profile_without_token(self):
        """Test accessing profile without token fails."""
        res = self.client.get(self.profile_url)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
