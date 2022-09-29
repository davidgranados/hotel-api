"""
Tests for models.
"""
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase

from core import models

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

    def test_create_recipe(self):
        """
        Test creating a new recipe is successful.
        """
        user = User.objects.create_user("test@example.com", "test123")
        title = "Test recipe"
        time_minutes = 5
        price = Decimal("5.00")
        description = "This is a test recipe."

        recipe = models.Recipe.objects.create(
            title=title,
            time_minutes=time_minutes,
            price=price,
            description=description,
            user=user,
        )

        self.assertEqual(recipe.title, title)
        self.assertEqual(recipe.time_minutes, time_minutes)
        self.assertEqual(recipe.price, price)
        self.assertEqual(recipe.description, description)
        self.assertEqual(recipe.user, user)

    def test_recipe_str(self):
        """
        Test the recipe string representation.
        """
        user = User.objects.create_user("test@example.com", "test123")
        title = "Test recipe"
        time_minutes = 5
        price = Decimal("5.00")
        description = "This is a test recipe."

        recipe = models.Recipe.objects.create(
            title=title,
            time_minutes=time_minutes,
            price=price,
            description=description,
            user=user,
        )

        self.assertEqual(str(recipe), title)

    def test_create_tag(self):
        """
        Test creating a new tag is successful.
        """
        user = create_user()
        tag = models.Tag.objects.create(user=user, name="Vegan")

        self.assertEqual(tag.name, "Vegan")
