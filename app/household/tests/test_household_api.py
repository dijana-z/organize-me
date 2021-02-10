from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient


HOUSEHOLD_URL = reverse('household:household-list')


class PublicHouseholdApiTests(TestCase):
    """Tests the public household API."""

    def setUp(self):
        self.client = APIClient()

    def test_get_household_not_successful(self):
        """Tests that getting the household information fails."""
        res = self.client.get(HOUSEHOLD_URL)

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
