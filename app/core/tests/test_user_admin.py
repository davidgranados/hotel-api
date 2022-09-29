from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

User = get_user_model()


class AdminSiteTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin_user = User.objects.create_superuser(email="admin@example.pe", password="123")
        self.user = User.objects.create_user(
            email="user@example.pe", password="123", first_name="test user name", last_name="test user last name"
        )
        self.client.force_login(self.admin_user)

    def test_users_listed(self):
        """
        Test that users are listed on user page.
        :return:
        """
        url = reverse("admin:core_customuser_changelist")
        res = self.client.get(url)

        self.assertContains(res, self.user.first_name)
        self.assertContains(res, self.user.last_name)
        self.assertContains(res, self.user.email)

    def test_user_change_page(self):
        """
        Test that the user change page works.
        :return: None
        """
        url = reverse("admin:core_customuser_change", args=[self.user.id])
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)

    def test_user_add_page(self):
        """
        Test that the user add page works.
        :return: None
        """
        url = reverse("admin:core_customuser_add")
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)
