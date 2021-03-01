from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient


from core.models import Household, Grocery


HOUSEHOLD_URL = reverse('household:household-list')


def get_household_detail_url(household_id):
    return reverse('household:household-detail', args=[household_id])


def create_sample_household():
    return Household.objects.create(name='Test Household')


def create_sample_grocery_item():
    household = create_sample_household()
    return Grocery.objects.create(
        name='Test Grocery',
        quantity=1,
        household=household
    )


class PublicHouseholdApiTests(TestCase):
    """Tests the public household API."""

    def setUp(self):
        self.client = APIClient()

    def test_get_household_not_successful(self):
        """Tests that getting the household information fails."""
        res = self.client.get(HOUSEHOLD_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_household_not_successful(self):
        """Tests that creating a new household fails."""
        payload = {
            'name': 'Test Household 1'
        }
        res = self.client.post(HOUSEHOLD_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateHouseholdApiTests(TestCase):
    """Tests the household API for authenticated users."""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email='test@test.com',
            password='TestPass123',
            name='Test User',
            household='Test Household'
        )
        self.client.force_authenticate(self.user)

    def test_get_household_successful(self):
        """Tests that getting the household information succeeds."""
        res = self.client.get(HOUSEHOLD_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(self.user.household.id, res.data[0]['id'])

    def test_create_new_household(self):
        """Tests that creating a new household is successful."""
        user = get_user_model().objects.create_user(
            email='test1@test.com',
            password='TestPass1',
            name='Test User 1',
        )
        self.client.force_authenticate(user)
        payload = {
            'name': 'Test Household 1'
        }
        res = self.client.post(HOUSEHOLD_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_patch_household(self):
        """Tests partial household update (PATCH)."""
        payload = {
            'name': 'Test Household Changed'
        }
        res = self.client.patch(get_household_detail_url(
            self.user.household.id), payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_put_household(self):
        payload = {
            'name': 'Test Household Changed',
            'grocery_list': [],
            'shopping_list': []
        }
        res = self.client.patch(get_household_detail_url(
            self.user.household.id), payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
