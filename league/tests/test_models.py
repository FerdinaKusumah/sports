from django.db import models
from django.test import TestCase

from league.models import Teams, Tournament


class TeamsModelTest(TestCase):
    def setUp(self):
        # Create a sample team for testing
        self.team = Teams.objects.create(name="Test Team")

    def test_team_str_representation(self):
        # Test the string representation of the Team model
        self.assertEqual(str(self.team), "Test Team")

    def test_team_creation(self):
        # Test the creation of a Team instance
        self.assertIsInstance(self.team, Teams)

    def test_team_name_unique_constraint(self):
        # Test that team names must be unique
        with self.assertRaises(Exception):
            Teams.objects.create(
                name="Test Team"
            )  # Attempt to create a team with the same name

    def test_team_model_manager(self):
        # Test the existence of the custom manager
        self.assertIsInstance(Teams.objects, models.Manager)

    def test_team_model_fields(self):
        # Test the correctness of model fields
        self.assertEqual(
            self.team._meta.get_field("id").get_internal_type(), "UUIDField"
        )
        self.assertEqual(self.team._meta.get_field("name").max_length, 255)
        self.assertTrue(self.team._meta.get_field("name").db_index)
        self.assertTrue(self.team._meta.get_field("name").unique)
        self.assertEqual(self.team._meta.ordering, ["name"])

    def test_team_model_meta(self):
        # Test the correctness of model Meta options
        self.assertEqual(self.team._meta.db_table, "teams")
        self.assertEqual(self.team._meta.verbose_name, "Team")
        self.assertEqual(self.team._meta.verbose_name_plural, "Team")

    def test_team_model_default_manager(self):
        # Test that the default manager is an instance of models.Manager
        self.assertIsInstance(Teams._default_manager, models.Manager)


class TournamentModelTest(TestCase):
    def setUp(self):
        # Create sample teams for testing
        self.home_team = Teams.objects.create(name="Home Team")
        self.away_team = Teams.objects.create(name="Away Team")

        # Create a sample tournament for testing
        self.tournament = Tournament.objects.create(
            home=self.home_team, away=self.away_team, home_score=2, away_score=1
        )

    def test_tournament_str_representation(self):
        # Test the string representation of the Tournament model
        expected_str = f"{self.home_team.name}:{self.away_team.name}"
        self.assertEqual(str(self.tournament), expected_str)

    def test_tournament_creation(self):
        # Test the creation of a Tournament instance
        self.assertIsInstance(self.tournament, Tournament)

    def test_tournament_default_scores(self):
        # Test that the default scores are set to 0
        tournament = Tournament.objects.create(home=self.home_team, away=self.away_team)
        self.assertEqual(tournament.home_score, 0)
        self.assertEqual(tournament.away_score, 0)

    def test_tournament_team_relationships(self):
        # Test the relationships between Tournament and Teams
        self.assertEqual(self.tournament.home, self.home_team)
        self.assertEqual(self.tournament.away, self.away_team)

    def test_tournament_model_manager(self):
        # Test the existence of the custom manager
        self.assertIsInstance(Tournament.objects, models.Manager)

    def test_tournament_model_meta(self):
        # Test the correctness of model Meta options
        self.assertEqual(self.tournament._meta.db_table, "tournaments")
        self.assertEqual(self.tournament._meta.verbose_name, "Tournaments")
        self.assertEqual(self.tournament._meta.verbose_name_plural, "Tournaments")
        self.assertEqual(self.tournament._meta.ordering, ["home"])

    def test_tournament_model_default_manager(self):
        # Test that the default manager is an instance of models.Manager
        self.assertIsInstance(Tournament._default_manager, models.Manager)
