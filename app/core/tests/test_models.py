from django.test import TestCase
from django.contrib.auth import get_user_model


def create_sample_user(email='test@test.com', password='TestPass123'):
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
