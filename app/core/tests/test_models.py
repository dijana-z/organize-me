from django.test import TestCase
from django.contrib.auth import get_user_model

from ..models import Household


def create_sample_user(email='test@test.com',
                       password='TestPass123'):
    """Creates a sample user."""
    return get_user_model().objects.create_user(email, password)


class ModelTests(TestCase):

    def test_create_user_with_email_ok(self):
        """Tests that creating a new user with an email is successful."""
        email = 'test@test.com'
        password = 'TestPass123'
        user = get_user_model().objects.create_user(
            email=email,
            password=password,
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_create_user_with_email_normalized(self):
        """Tests that the email for a new user is normalized."""
        email = 'test@TEST.com'
        password = 'TestPass123'
        user = get_user_model().objects.create_user(
            email=email,
            password=password,
        )

        e1, e2 = email.split('@')
        email = '@'.join([e1, e2.lower()])
        self.assertEqual(user.email, email.lower())

    def test_users_with_invalid_email_fails(self):
        """Tests that creating a user with invalid credentials fails."""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(
                email='',
                password='TestPass123',
            )

    def test_create_new_superuser(self):
        """Tests creating a new superuser."""
        superuser = get_user_model().objects.create_superuser(
            email='test@test.com',
            password='TestPass123',
        )

        self.assertTrue(superuser.is_staff)
        self.assertTrue(superuser.is_superuser)

    def test_create_new_household(self):
        """Tests creating a new household."""
        name = 'Test Household'
        household = Household.objects.create(
            name=name
        )

        self.assertEqual(household.name, name)

    def test_add_user_to_existing_household(self):
        """Tests adding a new user to household."""
        household_name = 'Test Household'

        user = get_user_model().objects.create_user(
            email='test@test.com',
            password='TestPass123',
            household=household_name,
        )

        self.assertEqual(user.household.name, household_name)

    def test_add_user_to_non_existing_household(self):
        """Tests that adding a user to non-existing household fails."""
        household = 'Test Household'
        user = get_user_model().objects.create_user(
            email='test@test.com',
            password='TestPass123',
            household=household,
        )

        self.assertEqual(user.household.name, household)

    def test_multiple_users_in_one_household(self):
        """Tests adding multiple users to one household."""
        household = Household.objects.get_or_create(name='Test Household')[0]
        user1 = get_user_model().objects.create_user(
            email='test@test.com',
            password='TestPass123',
            household=household.name,
        )
        user2 = get_user_model().objects.create_user(
            email='test1@test1.com',
            password='TestPass456',
            household=household.name,
        )

        self.assertEqual(user1.household.name, household.name)
        self.assertEqual(user2.household.name, household.name)
