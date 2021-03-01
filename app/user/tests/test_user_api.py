from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')
ME_URL = reverse('user:me')


def create_user(**kwargs):
    return get_user_model().objects.create_user(**kwargs)


class PublicUserApiTests(TestCase):
    """Tests the public user API."""

    def setUp(self):
        self.client = APIClient()

    def test_create_valid_user_success(self):
        """Tests that creating user with valid data is successful."""
        payload = {
            'email': 'test@test.com',
            'password': 'TestPass123',
            'name': 'Test User'
        }
        res = self.client.post(CREATE_USER_URL, payload)
        user = get_user_model().objects.get(**res.data)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data)

    def test_create_duplicate_user_fails(self):
        """Tests that creating a duplicate user fails."""
        payload = {
            'email': 'test@test.com',
            'password': 'TestPass123',
            'name': 'Test User'
        }
        create_user(**payload)
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short(self):
        """Tests that creating a user with too short password fails."""
        payload = {
            'email': 'test@test.com',
            'password': 'Test',
            'name': 'Test User'
        }
        res = self.client.post(CREATE_USER_URL, payload)
        user_exists = get_user_model().objects.filter(
            email=payload['email']).exists()

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(user_exists)

    def test_create_token_for_user(self):
        """Tests that a token is created for the user."""
        payload = {
            'email': 'test@test.com',
            'password': 'TestPass123',
            'name': 'Test User'
        }
        create_user(**payload)
        res = self.client.post(TOKEN_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn('token', res.data)

    def test_create_token_invalid_credentials(self):
        """Tests that creating a token with invalid credentials fails."""
        payload = {
            'email': '',
            'password': 'TestPass123',
            'name': 'Test User'
        }
        res = self.client.post(TOKEN_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn('token', res.data)

    def test_create_token_no_user(self):
        """Tests that creating a token for a user that doesn't exist fails."""
        payload = {
            'email': 'test@test.com',
            'password': 'TestPass123',
            'name': 'Test User'
        }
        res = self.client.post(TOKEN_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn('token', res.data)

    def test_create_token_missing_fields(self):
        """Tests that email and password are required for creating a token."""
        payload = {
            'email': 'test@test.com',
            'password': '',
            'name': 'Test User'
        }
        res = self.client.post(TOKEN_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn('token', res.data)

    def test_retrieve_user_unauthorized(self):
        """Tests that authentication is required for retrieving an user."""
        res = self.client.get(ME_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateUserApiTests(TestCase):
    """Tests the authenticated user API."""

    def setUp(self):
        self.client = APIClient()
        self.user = create_user(
            email='test@test.com',
            password='TestPass123',
            name='Test User',
        )
        self.client.force_authenticate(user=self.user)

    def test_retrieve_user(self):
        """Tests that retrieving user is successful."""
        res = self.client.get(ME_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data.get('email'), self.user.email)

    def test_post_not_allowed(self):
        """Tests that POST is not allowed for ME url."""
        payload = {
            'email': 'test1@test1.com',
            'password': 'TestPass456',
            'name': 'Test User 1'
        }
        res = self.client.post(ME_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_user_profile(self):
        """Tests that updating user profile is successful."""
        payload = {
            'name': 'New Name',
            'password': 'NewPass123'
        }

        res = self.client.patch(ME_URL, payload)
        self.user.refresh_from_db()

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data.get('name'), payload.get('name'))
        self.assertTrue(self.user.check_password(payload['password']))
