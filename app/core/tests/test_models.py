"""
Tests for models.
"""
from django.contrib.auth import get_user_model
from django.test import TestCase

User = get_user_model()


def create_user(email="user@example.com", password="test123"):
    """Create and return a new user."""
    return User.objects.create_user(email=email, password=password)


class ModelTests(TestCase):
    """
    Tests for models.
    """

    def test_create_user_with_email_successful(self):
        """
        Test creating a new user with an email is successful.
        """
        email = "test@example"
        password = "Testpass123"
        user = User.objects.create_user(email=email, password=password)

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """
        Test the email for a new user is normalized.
        """
        sample_emails = [
            ["test1@EXAMPLE.com", "test1@example.com"],
            ["Test2@EXAMPLE.com", "Test2@example.com"],
            ["TEST3@EXAMPLE.com", "TEST3@example.com"],
            ["test4@EXAMPLE.com", "test4@example.com"],
        ]

        for email, expected in sample_emails:
            user = User.objects.create_user(email=email, password="test123")

            self.assertEqual(user.email, expected)

        email = "test@EXAMPLE.com"
        user = User.objects.create_user(email, "test123")

        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        """
        Test creating user with no email raises error.
        """
        with self.assertRaises(ValueError):
            User.objects.create_user(None, "test123")

    def test_create_new_superuser(self):
        """
        Test creating a new superuser.
        """
        user = User.objects.create_superuser("test@example.com", "test123")

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
