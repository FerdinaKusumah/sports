from unittest.mock import patch

from django.test import TestCase

from league.backends import StatisticController
from league.models import Teams, Tournament


class StatisticControllerTest(TestCase):
    def setUp(self):
        # Sample teams for testing
        self.team1 = Teams.objects.create(name="Team 1")
        self.team2 = Teams.objects.create(name="Team 2")
        self.team3 = Teams.objects.create(name="Team 3")

    def create_tournament(self, home_team, away_team, home_score, away_score):
        """Helper method to create a tournament with specified teams and scores"""
        return Tournament.objects.create(
            home=home_team, away=away_team, home_score=home_score, away_score=away_score
        )

    def test_get_statistic_method(self):
        # Test the get_statistic method

        # Create sample tournament data for testing
        self.create_tournament(self.team1, self.team2, 2, 1)
        self.create_tournament(self.team2, self.team1, 0, 2)
        self.create_tournament(self.team1, self.team3, 1, 1)

        # Mock the Teams.objects.all method to return the sample teams
        with patch.object(
            Teams.objects, "all", return_value=[self.team1, self.team2, self.team3]
        ):
            controller = StatisticController()
            result = controller.get_statistic()

            # Ensure the result is a list
            self.assertIsInstance(result, list)

            # Ensure the result contains the correct team statistics
            self.assertEqual(len(result), 3)

            # Team 1
            self.assertEqual(result[0]["name"], "Team 1")
            self.assertEqual(result[0]["p"], 3)  # Total matches played
            self.assertEqual(result[0]["w"], 2)  # Total matches won
            self.assertEqual(result[0]["d"], 1)  # Total matches drawn
            self.assertEqual(result[0]["l"], 0)  # Total matches lost
            self.assertEqual(result[0]["pts"], 7)  # Total points

            # Team 2
            self.assertEqual(result[1]["name"], "Team 2")
            self.assertEqual(result[1]["p"], 2)
            self.assertEqual(result[1]["w"], 0)
            self.assertEqual(result[1]["d"], 0)
            self.assertEqual(result[1]["l"], 2)
            self.assertEqual(result[1]["pts"], 0)

            # Team 3
            self.assertEqual(result[2]["name"], "Team 3")
            self.assertEqual(result[2]["p"], 1)
            self.assertEqual(result[2]["w"], 0)
            self.assertEqual(result[2]["d"], 1)
            self.assertEqual(result[2]["l"], 0)
            self.assertEqual(result[2]["pts"], 1)
