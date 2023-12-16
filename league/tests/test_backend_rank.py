from unittest.mock import patch

from django.test import TestCase

from league.backends import RankController, StatisticController
from league.models import Teams, Tournament


class RankControllerTest(TestCase):
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

    def test_calculate_rank_method(self):
        # Test the calculate_rank method

        # Create sample tournament data for testing
        self.create_tournament(self.team1, self.team2, 2, 1)
        self.create_tournament(self.team2, self.team1, 0, 2)
        self.create_tournament(self.team1, self.team3, 1, 1)

        # Mock the StatisticController.get_statistic method
        with patch.object(
            StatisticController,
            "get_statistic",
            return_value=[
                {"name": "Team 1", "p": 2, "w": 1, "d": 1, "l": 0, "pts": 4},
                {"name": "Team 2", "p": 2, "w": 1, "d": 0, "l": 1, "pts": 3},
                {"name": "Team 3", "p": 1, "w": 0, "d": 1, "l": 0, "pts": 1},
            ],
        ):
            controller = RankController()
            RankController.max_rank = 3
            result = controller.calculate_rank()

            # Ensure the result is a list
            self.assertIsInstance(result, list)

            # Ensure the result contains the correct team ranks
            self.assertEqual(len(result), RankController.max_rank)

            # Team 1
            self.assertEqual(result[0]["rank"], 1)
            self.assertEqual(result[0]["team"], "Team 1")
            self.assertEqual(result[0]["point"], 4)

            # Team 2
            self.assertEqual(result[1]["rank"], 2)
            self.assertEqual(result[1]["team"], "Team 2")
            self.assertEqual(result[1]["point"], 3)

            # Team 3
            self.assertEqual(result[2]["rank"], 3)
            self.assertEqual(result[2]["team"], "Team 3")
            self.assertEqual(result[2]["point"], 1)
