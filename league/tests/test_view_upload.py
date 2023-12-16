from http import HTTPStatus

from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse


class UploadViewTest(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )

    def login(self):
        # Log in the test user
        self.client.login(username="testuser", password="testpassword")

    def test_unauthenticated_access(self):
        url = reverse("upload")
        response = self.client.get(url)
        self.assertRedirects(response, f"{reverse('login')}?redirect_to={url}")

    def test_get_method_authenticated_user(self):
        self.login()
        url = reverse("upload")
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response["Content-Type"], "application/octet-stream")
        self.assertIn("Content-Disposition", response)
        self.assertIn("attachment; filename=", response["Content-Disposition"])

    def test_post_method_authenticated_user(self):
        self.login()
        # Prepare a test CSV file
        csv_content = "team_1_name,team_2_name,team_1_score,team_2_score\nTeam A,Team B,2,1\nTeam C,Team D,3,3"
        csv_file = SimpleUploadedFile("test_file.csv", bytes(csv_content, "utf-8"))

        url = reverse("upload")
        response = self.client.post(url, {"file": csv_file})
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertIn("status", response.json())
        self.assertEqual(response.json()["status"], "ok")
