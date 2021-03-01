from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Household, Grocery

from household.serializers import GrocerySerializer


GROCERY_URL = reverse('household:grocery-list')
GROCERY_LIST_URL = reverse('household:grocerylist-list')
SHOPPING_LIST_URL = reverse('household:shoppinglist-list')


def get_grocery_detail_url(grocery_id):
    return reverse('household:grocery-detail', args=[grocery_id])


def get_user_household(user):
    return Household.objects.filter(
        name=user.household.name).first()


def create_test_grocery_for_user(user):
    return Grocery.objects.create(
            name='Test Grocery',
            quantity=1,
            household=get_user_household(user)
        )


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

    def test_post_grocery(self):
        """Tests creating a new grocery."""
        payload = {
            'name': 'Test Grocery',
            'quantity': 3,
        }

        res = self.client.post(GROCERY_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_patch_grocery(self):
        """Tests updating a grocery via PATCH."""
        grocery = create_test_grocery_for_user(self.user)

        payload = {
            'name': 'Test Grocery 1',
        }

        self.client.patch(get_grocery_detail_url(grocery.id), payload)
        grocery.refresh_from_db()

        self.assertEqual(grocery.name, payload['name'])

    def test_put_grocery(self):
        """Tests updating a grocery via PUT."""
        household = get_user_household(self.user)
        grocery = create_test_grocery_for_user(self.user)

        payload = {
            'name': 'Test Grocery 1',
            'quantity': 2,
            'household': household.id
        }

        self.client.patch(get_grocery_detail_url(grocery.id), payload)
        grocery.refresh_from_db()

        self.assertEqual(grocery.name, payload['name'])

    def test_view_grocery_detail(self):
        """Tests viewing a grocery detail."""
        grocery = create_test_grocery_for_user(self.user)

        res = self.client.get(get_grocery_detail_url(grocery.id))
        serializer = GrocerySerializer(grocery)

        self.assertEqual(res.data, serializer.data)

    def test_view_grocery_list(self):
        """Tests getting the grocery list from household."""
        res = self.client.get(GROCERY_LIST_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_view_shopping_list(self):
        """Tests getting the shopping list from household."""
        res = self.client.get(SHOPPING_LIST_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_add_grocery_to_grocery_list(self):
        """Tests adding grocery to grocery list."""
        payload = {
            'name': 'Test Grocery',
            'quantity': 1
        }
        res = self.client.post(GROCERY_LIST_URL, payload)
        household = get_user_household(self.user)
        household.refresh_from_db()
        grocery = household.grocery_list.all().first()
        serializer = GrocerySerializer(grocery)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(payload['name'], serializer.data['name'])
        self.assertEqual(payload['quantity'], serializer.data['quantity'])

    def test_add_grocery_to_shopping_list(self):
        """Tests adding grocery to grocery list."""
        payload = {
            'name': 'Test Grocery',
            'quantity': 1
        }
        res = self.client.post(SHOPPING_LIST_URL, payload)
        household = get_user_household(self.user)
        household.refresh_from_db()
        grocery = household.shopping_list.all().first()
        serializer = GrocerySerializer(grocery)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(payload['name'], serializer.data['name'])
        self.assertEqual(payload['quantity'], serializer.data['quantity'])

    def test_delete_grocery(self):
        """Tests deleting a grocery item."""
        payload = {
            'name': 'Test Grocery',
            'quantity': 5,
        }
        res = self.client.post(GROCERY_URL, payload)
        res = self.client.delete(get_grocery_detail_url(res.data['id']))

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)

    def test_adding_empty_grocery_name(self):
        """Tests that creating a grocery without a name fails."""
        payload = {
            'name': '',
            'quantity': 5,
        }
        res = self.client.post(GROCERY_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_adding_invalid_grocery_quantity(self):
        """Tests that creating a grocery with invalid quantity fails."""
        payload = {
            'name': 'Test',
            'quantity': -10,
        }
        res = self.client.post(GROCERY_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
