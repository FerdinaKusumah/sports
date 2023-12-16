import uuid
from unittest.mock import patch, Mock

from django.test import TestCase

from league.backends import UploadController
from league.models import Teams, Tournament


class UploadControllerTest(TestCase):
    def setUp(self):
        # Sample records for testing
        self.records = [
            {
                "team_1_name": "Team A",
                "team_2_name": "Team B",
                "team_1_score": 2,
                "team_2_score": 1,
            },
            {
                "team_1_name": "Team C",
                "team_2_name": "Team D",
                "team_1_score": 0,
                "team_2_score": 2,
            },
        ]

    def test_get_file_path_method(self):
        # Test the get_file_path method
        controller = UploadController(self.records)
        result = controller.get_file_path()

        # Ensure the result is the correct file path
        self.assertEqual(result, "templates/upload/league.csv")

    def test_populate_team_ids_method(self):
        # Test the populate_team_ids method

        # Mock the Teams.objects.filter method to return sample teams
        with patch.object(
            Teams.objects,
            "filter",
            return_value=[
                Mock(name="Team A", id=uuid.uuid4()),
                Mock(name="Team B", id=uuid.uuid4()),
                Mock(name="Team C", id=uuid.uuid4()),
            ],
        ):
            controller = UploadController(self.records)
            result = controller.populate_team_ids()

            # Ensure the result is a dictionary
            self.assertIsInstance(result, dict)

            # Ensure the result contains the correct team data
            self.assertEqual(len(result), 4)
            self.assertIn("Team A", result)
            self.assertIn("Team B", result)
            self.assertIn("Team C", result)
            self.assertIn("Team D", result)

    def test_store_method(self):
        # Test the store method without mocking

        # Ensure there are no existing teams and tournaments in the database
        self.assertEqual(Teams.objects.count(), 0)
        self.assertEqual(Tournament.objects.count(), 0)

        # Create an instance of UploadController and call the store method
        controller = UploadController(self.records)
        result = controller.store()

        # Ensure the store method returns True
        self.assertTrue(result)

        # Ensure the teams and tournaments are created in the database
        self.assertEqual(Teams.objects.count(), 4)  # Assuming 4 teams in records
        self.assertEqual(Tournament.objects.count(), len(self.records))

        # Retrieve and verify data from the database
        team_names = set([team["name"] for team in Teams.objects.values()])
        self.assertEqual(team_names, {"Team A", "Team B", "Team C", "Team D"})

        for record in self.records:
            tournament = Tournament.objects.get(
                home__name=record["team_1_name"],
                away__name=record["team_2_name"],
                home_score=record["team_1_score"],
                away_score=record["team_2_score"],
            )
            self.assertIsNotNone(tournament)
