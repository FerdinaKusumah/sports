from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages
from django.test import TestCase, Client
from django.urls import reverse


class LoginViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.login_url = reverse("login")
        self.home_url = reverse("home")
        self.user_data = {
            "username": "testuser",
            "password": "testpassword",
        }
        self.user = get_user_model().objects.create_user(**self.user_data)

    def test_render_login_page(self):
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "auth/login.html")

    def test_login_with_valid_credentials(self):
        response = self.client.post(self.login_url, data=self.user_data, follow=True)
        self.assertRedirects(response, self.home_url)
        self.assertTrue(response.context["user"].is_authenticated)

    def test_login_with_invalid_credentials(self):
        invalid_data = {"username": "invaliduser", "password": "invalidpassword"}
        response = self.client.post(self.login_url, data=invalid_data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "auth/login.html")
        self.assertFalse(response.context["user"].is_authenticated)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "Invalid username or password")

    def test_redirect_authenticated_user(self):
        # Log in the user first
        self.client.login(username="testuser", password="testpassword")

        # Try to access the login page again
        response = self.client.get(self.login_url)
        self.assertRedirects(response, self.home_url)
