import json
from http import HTTPStatus
from uuid import uuid4

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from league.models import Teams


class TeamsViewTest(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )
        # Create a team
        self.team = Teams.objects.create(id=uuid4(), name="Team A")

    def login(self):
        # Log in the test user
        self.client.login(username="testuser", password="testpassword")

    def test_post_method(self):
        self.login()  # Log in before making a request
        url = reverse("team")
        data = {"name": "Team B"}
        response = self.client.post(
            url, json.dumps(data), content_type="application/json"
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.json(), {"status": "ok"})
        self.assertTrue(Teams.objects.filter(name="Team B").exists())

    def test_put_method(self):
        self.login()
        team_id = self.team.id
        url = reverse("team-update", kwargs={"id": team_id})
        data = {"name": "Updated Team A"}
        response = self.client.put(
            url, json.dumps(data), content_type="application/json"
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.json(), {"status": "ok"})
        self.assertTrue(Teams.objects.filter(name="Updated Team A").exists())

    def test_delete_method(self):
        self.login()
        team_id = self.team.id
        url = reverse("team-update", kwargs={"id": team_id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.json(), {"status": "ok"})
        self.assertFalse(Teams.objects.filter(id=team_id).exists())

    def test_get_method(self):
        self.login()
        url = reverse("team")
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertIn("data", response.json())
