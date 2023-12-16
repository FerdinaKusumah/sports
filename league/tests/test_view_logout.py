from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse


class LogoutViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.logout_url = reverse("logout")
        self.login_url = reverse("login")
        self.home_url = reverse("home")
        self.user_data = {
            "username": "testuser",
            "password": "testpassword",
        }
        self.user = get_user_model().objects.create_user(**self.user_data)

    def test_logout_authenticated_user(self):
        # Log in the user first
        self.client.login(username="testuser", password="testpassword")

        # Logout the user with a POST request
        response = self.client.post(self.logout_url, follow=True)
        self.assertRedirects(response, self.login_url)
        self.assertFalse(response.context["user"].is_authenticated)

    def test_logout_unauthenticated_user(self):
        # Attempt to access the logout page without logging in
        response = self.client.post(self.logout_url, follow=True)
        self.assertRedirects(response, self.login_url)

    def test_redirect_after_logout(self):
        # Log in the user first
        self.client.login(username="testuser", password="testpassword")

        # Logout the user and check the redirection
        response = self.client.post(self.logout_url, follow=True)
        self.assertRedirects(response, self.login_url)

        # Attempt to access the logout page again
        response_after_logout = self.client.post(self.logout_url, follow=True)
        self.assertRedirects(response_after_logout, self.login_url)
