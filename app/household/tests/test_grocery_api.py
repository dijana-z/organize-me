from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

# from core.models import Household

# from household.serializers import GrocerySerializer


GROCERY_URL = reverse('household:grocery-list')
GROCERY_LIST_URL = reverse('household:grocerylist-list')
SHOPPING_LIST_URL = reverse('household:shoppinglist-list')


class PublicGroceryApiTests(TestCase):
    """Tests the publicly available grocery API."""

    def setUp(self):
        self.client = APIClient()

    def test_login_required_grocery(self):
        """Tests that login is required for retrieving groceries."""
        res = self.client.get(GROCERY_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_login_required_grocery_list(self):
        """Tests that login is required for retrieving grocery list."""
        res = self.client.get(GROCERY_LIST_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_login_required_shopping_list(self):
        """Tests that login is required for retrieving shopping list."""
        res = self.client.get(SHOPPING_LIST_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateGroceryApiTests(TestCase):
    """Tests the grocery API for authenticated users."""

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email='test@test.com',
            password='TestPass123',
            name='Test User',
            household='Test Household'
        )
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_get_grocery(self):
        """Tests that getting grocery succeeds."""
        res = self.client.get(GROCERY_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)

    # def test_post_grocery(self):
    #     household = Household.objects.filter(name=self.user.household.name)
    #     payload = {
    #         'name': 'Test Grocery',
    #         'quantity': 2,
    #         'household': household.name
    #     }
    #
    #     res = self.client.post(GROCERY_URL, payload)
    #
    #     self.assertEqual(res.status_code, status.HTTP_201_CREATED)
