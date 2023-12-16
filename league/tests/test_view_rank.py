from http import HTTPStatus
from uuid import uuid4

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from league.models import Teams, Tournament


class RankViewTest(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )
        # Create some teams
        self.team_a = Teams.objects.create(id=uuid4(), name="Team A")
        self.team_b = Teams.objects.create(id=uuid4(), name="Team B")
        # Create a tournament with results
        self.tournament_1 = Tournament.objects.create(
            id=uuid4(), home=self.team_a, away=self.team_b, home_score=2, away_score=1
        )
        self.tournament_2 = Tournament.objects.create(
            id=uuid4(), home=self.team_b, away=self.team_a, home_score=0, away_score=2
        )

    def login(self):
        # Log in the test user
        self.client.login(username="testuser", password="testpassword")

    def test_unauthenticated_access(self):
        url = reverse("rank")
        response = self.client.get(url)
        self.assertRedirects(response, f"{reverse('login')}?redirect_to={url}")

    def test_get_method_authenticated_user(self):
        self.login()
        url = reverse("rank")
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertIn("data", response.json())
        self.assertIsInstance(response.json()["data"], list)
        expected_structure = ["rank", "team", "point"]
        self.assertListEqual(
            list(response.json()["data"][0].keys()), expected_structure
        )
