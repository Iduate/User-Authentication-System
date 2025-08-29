from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from unittest.mock import patch, MagicMock

User = get_user_model()

class PasswordResetTests(TestCase):
    """Test the password reset functionality."""

    def setUp(self):
        self.client = APIClient()
        self.reset_request_url = '/api/v1/users/password-reset/'
        self.reset_confirm_url = '/api/v1/users/password-reset/confirm/'
        
        # Create a test user for password reset tests
        self.test_user = User.objects.create_user(
            email='resetuser@example.com',
            password='oldpassword123',
            full_name='Reset Test User'
        )

    @patch('users.views.generate_password_reset_token')
    def test_password_reset_request_existing_user(self, mock_generate_token):
        """Test password reset request for an existing user."""
        mock_generate_token.return_value = 'test-token-123456'
        
        payload = {
            'email': 'resetuser@example.com'
        }
        response = self.client.post(self.reset_request_url, payload)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('detail', response.data)
        self.assertIn('token', response.data)  # In a real app, token would be sent via email
        mock_generate_token.assert_called_once_with(self.test_user.id)

    def test_password_reset_request_nonexistent_user(self):
        """Test password reset request for a non-existent user."""
        payload = {
            'email': 'nonexistent@example.com'
        }
        response = self.client.post(self.reset_request_url, payload)
        
        # Should still return 200 OK for security reasons
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('detail', response.data)
        # The message shouldn't reveal whether the email exists
        self.assertNotIn('token', response.data)

    @patch('users.views.validate_password_reset_token')
    def test_password_reset_confirm_valid_token(self, mock_validate_token):
        """Test password reset confirmation with a valid token."""
        mock_validate_token.return_value = self.test_user.id
        
        payload = {
            'token': 'valid-token-123456',
            'new_password': 'newpassword123',
            'new_password_confirm': 'newpassword123'
        }
        response = self.client.post(self.reset_confirm_url, payload)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('detail', response.data)
        
        # Check if password was actually changed
        self.test_user.refresh_from_db()
        self.assertTrue(self.test_user.check_password('newpassword123'))
        
        # Check that token was validated
        mock_validate_token.assert_called_once_with('valid-token-123456')

    @patch('users.views.validate_password_reset_token')
    def test_password_reset_confirm_invalid_token(self, mock_validate_token):
        """Test password reset confirmation with an invalid token."""
        mock_validate_token.return_value = None
        
        payload = {
            'token': 'invalid-token',
            'new_password': 'newpassword123',
            'new_password_confirm': 'newpassword123'
        }
        response = self.client.post(self.reset_confirm_url, payload)
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('detail', response.data)
        
        # Check that password was not changed
        self.test_user.refresh_from_db()
        self.assertFalse(self.test_user.check_password('newpassword123'))
        self.assertTrue(self.test_user.check_password('oldpassword123'))

    def test_password_reset_confirm_password_mismatch(self):
        """Test password reset confirmation with mismatched passwords."""
        payload = {
            'token': 'some-token',
            'new_password': 'newpassword123',
            'new_password_confirm': 'differentpassword123'
        }
        response = self.client.post(self.reset_confirm_url, payload)
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('non_field_errors', response.data)

    @patch('users.views.PasswordResetRateThrottle.allow_request')
    def test_password_reset_rate_limiting(self, mock_allow_request):
        """Test rate limiting on the password reset endpoint."""
        # Set up the mock to simulate rate limit exceeded
        mock_allow_request.return_value = False
        
        payload = {
            'email': 'resetuser@example.com'
        }
        response = self.client.post(self.reset_request_url, payload)
        
        self.assertEqual(response.status_code, status.HTTP_429_TOO_MANY_REQUESTS)
        mock_allow_request.assert_called_once()
