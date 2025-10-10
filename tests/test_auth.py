"""
Tests for authentication endpoints.
"""
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from backend.models import User


class UserModelTestCase(TestCase):
    """Tests for User model."""

    def test_create_user(self):
        """Test creating a user."""
        user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.assertEqual(user.email, 'test@example.com')
        self.assertEqual(user.username, 'testuser')
        self.assertTrue(user.check_password('testpass123'))
        self.assertFalse(user.email_verified)
        self.assertFalse(user.two_factor_enabled)

    def test_user_str_representation(self):
        """Test user string representation."""
        user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.assertEqual(str(user), 'test@example.com')

    def test_has_plaid_connection(self):
        """Test has_plaid_connection property."""
        user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.assertFalse(user.has_plaid_connection)

        user.plaid_access_token = 'test_token'
        user.plaid_item_id = 'test_item_id'
        user.save()
        self.assertTrue(user.has_plaid_connection)


class RegistrationTestCase(APITestCase):
    """Tests for user registration endpoint."""

    def setUp(self):
        self.client = APIClient()
        self.register_url = reverse('backend:register')

    def test_register_user_success(self):
        """Test successful user registration."""
        data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'SecurePass123!',
            'password_confirm': 'SecurePass123!',
            'first_name': 'John',
            'last_name': 'Doe'
        }
        response = self.client.post(self.register_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('tokens', response.data)
        self.assertIn('user', response.data)
        self.assertEqual(response.data['user']['email'], 'newuser@example.com')

    def test_register_user_password_mismatch(self):
        """Test registration with mismatched passwords."""
        data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'SecurePass123!',
            'password_confirm': 'DifferentPass123!',
        }
        response = self.client.post(self.register_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_user_duplicate_email(self):
        """Test registration with duplicate email."""
        User.objects.create_user(
            username='existing',
            email='existing@example.com',
            password='testpass123'
        )
        data = {
            'username': 'newuser',
            'email': 'existing@example.com',
            'password': 'SecurePass123!',
            'password_confirm': 'SecurePass123!',
        }
        response = self.client.post(self.register_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class LoginTestCase(APITestCase):
    """Tests for user login endpoint."""

    def setUp(self):
        self.client = APIClient()
        self.login_url = reverse('backend:login')
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )

    def test_login_success(self):
        """Test successful login."""
        data = {
            'email': 'test@example.com',
            'password': 'testpass123'
        }
        response = self.client.post(self.login_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
        self.assertIn('user', response.data)

    def test_login_invalid_credentials(self):
        """Test login with invalid credentials."""
        data = {
            'email': 'test@example.com',
            'password': 'wrongpassword'
        }
        response = self.client.post(self.login_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class UserProfileTestCase(APITestCase):
    """Tests for user profile endpoints."""

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.client.force_authenticate(user=self.user)

    def test_get_current_user(self):
        """Test getting current user profile."""
        url = reverse('backend:current_user')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], 'test@example.com')

    def test_update_user_profile(self):
        """Test updating user profile."""
        url = reverse('backend:update_user')
        data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'phone_number': '+1234567890'
        }
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, 'John')
        self.assertEqual(self.user.last_name, 'Doe')

    def test_change_password_success(self):
        """Test successful password change."""
        url = reverse('backend:change_password')
        data = {
            'old_password': 'testpass123',
            'new_password': 'NewSecurePass123!',
            'new_password_confirm': 'NewSecurePass123!'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('NewSecurePass123!'))

    def test_change_password_wrong_old_password(self):
        """Test password change with incorrect old password."""
        url = reverse('backend:change_password')
        data = {
            'old_password': 'wrongpassword',
            'new_password': 'NewSecurePass123!',
            'new_password_confirm': 'NewSecurePass123!'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_unauthenticated_access(self):
        """Test that unauthenticated users cannot access protected endpoints."""
        self.client.force_authenticate(user=None)
        url = reverse('backend:current_user')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
