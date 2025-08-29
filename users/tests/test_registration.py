from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from unittest.mock import patch, MagicMock
import json

User = get_user_model()

class RegistrationTests(TestCase):
    """Test the user registration API."""

    def setUp(self):
        self.client = APIClient()
        self.register_url = '/api/v1/users/register/'

    def test_user_registration_successful(self):
        """Test successful user registration with valid data."""
        payload = {
            'email': 'newuser@example.com',
            'password': 'securepass123',
            'password_confirm': 'securepass123',
            'full_name': 'New Test User',
        }
        response = self.client.post(self.register_url, payload)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(email='newuser@example.com').exists())
        
        # Check if tokens are returned
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
        self.assertIn('user', response.data)
        
        # Check user data in response
        self.assertEqual(response.data['user']['email'], 'newuser@example.com')
        self.assertEqual(response.data['user']['full_name'], 'New Test User')
        self.assertNotIn('password', response.data['user'])

    def test_user_registration_with_existing_email(self):
        """Test user registration fails with an email that already exists."""
        # Create a user first
        User.objects.create_user(
            email='existing@example.com',
            password='password123',
            full_name='Existing User'
        )
        
        # Attempt to register with the same email
        payload = {
            'email': 'existing@example.com',
            'password': 'securepass123',
            'password_confirm': 'securepass123',
            'full_name': 'Another User',
        }
        response = self.client.post(self.register_url, payload)
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', response.data)

    def test_user_registration_weak_password(self):
        """Test registration with a weak password fails."""
        payload = {
            'email': 'newuser@example.com',
            'password': '123456',
            'password_confirm': '123456',
            'full_name': 'New Test User',
        }
        response = self.client.post(self.register_url, payload)
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('password', response.data)
        self.assertFalse(User.objects.filter(email='newuser@example.com').exists())

    def test_user_registration_password_mismatch(self):
        """Test registration fails when passwords don't match."""
        payload = {
            'email': 'newuser@example.com',
            'password': 'securepass123',
            'password_confirm': 'differentpass123',
            'full_name': 'New Test User',
        }
        response = self.client.post(self.register_url, payload)
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('non_field_errors', response.data)
        self.assertFalse(User.objects.filter(email='newuser@example.com').exists())

    def test_user_registration_missing_fields(self):
        """Test registration fails when required fields are missing."""
        # Test without email
        payload = {
            'password': 'securepass123',
            'password_confirm': 'securepass123',
            'full_name': 'New Test User',
        }
        response = self.client.post(self.register_url, payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
        # Test without password
        payload = {
            'email': 'newuser@example.com',
            'password_confirm': 'securepass123',
            'full_name': 'New Test User',
        }
        response = self.client.post(self.register_url, payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
        # Test without full name
        payload = {
            'email': 'newuser@example.com',
            'password': 'securepass123',
            'password_confirm': 'securepass123',
        }
        response = self.client.post(self.register_url, payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
