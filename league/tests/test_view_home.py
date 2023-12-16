from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse


class HomeViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.home_url = reverse("home")
        self.login_url = reverse("login")
        self.user_data = {
            "username": "testuser",
            "password": "testpassword",
        }
        self.user = get_user_model().objects.create_user(**self.user_data)

    def test_access_home_view_authenticated_user(self):
        # Log in the user first
        self.client.login(username="testuser", password="testpassword")

        # Access the home view
        response = self.client.get(self.home_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "home/index.html")

    def test_access_home_view_unauthenticated_user(self):
        # Attempt to access the home view without logging in
        response = self.client.get(self.home_url)

        # Verify that the user is redirected to the login page with the correct query parameter
        expected_url = f"{self.login_url}?redirect_to={self.home_url}"
        self.assertRedirects(response, expected_url, fetch_redirect_response=False)
