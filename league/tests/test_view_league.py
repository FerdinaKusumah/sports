import json

from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from league.models import Teams, Tournament


class LeagueViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.login_url = reverse("login")
        self.user_data = {
            "username": "testuser",
            "password": "testpassword",
        }
        self.user = get_user_model().objects.create_user(**self.user_data)
        self.team1 = Teams.objects.create(name="Team 1")
        self.team2 = Teams.objects.create(name="Team 2")
        self.tournament_data = {
            "home_id": self.team1.id,
            "away_id": self.team2.id,
            "home_score": 2,
            "away_score": 1,
        }
        self.tournament = Tournament.objects.create(**self.tournament_data)

    def test_post_method(self):
        self.client.login(username="testuser", password="testpassword")
        url = reverse("league")
        data = {
            "home_id": str(self.team1.id),
            "away_id": str(self.team2.id),
            "home_score": 3,
            "away_score": 2,
        }
        response = self.client.post(
            url, json.dumps(data), content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], "ok")

    def test_put_method(self):
        self.client.login(username="testuser", password="testpassword")
        url = reverse("league-update", kwargs={"id": str(self.tournament.id)})
        data = {"home_score": 4, "away_score": 2}
        response = self.client.put(
            url, json.dumps(data), content_type="application/json"
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["message"], "Home id is required")

    def test_delete_method(self):
        self.client.login(username="testuser", password="testpassword")
        url = reverse("league-update", kwargs={"id": str(self.tournament.id)})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], "ok")
