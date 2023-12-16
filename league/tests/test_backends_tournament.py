import uuid
from unittest.mock import patch, Mock

from django.test import TestCase

from league.backends import TournamentDtoRequest, TournamentController
from league.models import Tournament, Teams


class TournamentDtoRequestTest(TestCase):
    def setUp(self):
        # Sample data for testing
        self.dto_data = {
            "home_id": "home_team_id",
            "home_score": 2,
            "away_id": "away_team_id",
            "away_score": 1,
        }

    def test_create_tournament_dto_instance(self):
        # Test the creation of a TournamentDtoRequest instance
        tournament_dto = TournamentDtoRequest(
            home_id=self.dto_data["home_id"],
            home_score=self.dto_data["home_score"],
            away_id=self.dto_data["away_id"],
            away_score=self.dto_data["away_score"],
        )
        self.assertIsInstance(tournament_dto, TournamentDtoRequest)

    def test_from_payload_method(self):
        # Test the from_payload method
        tournament_dto = TournamentDtoRequest.from_payload(**self.dto_data)
        self.assertIsInstance(tournament_dto, TournamentDtoRequest)
        self.assertEqual(tournament_dto.home_id, self.dto_data["home_id"])
        self.assertEqual(tournament_dto.home_score, self.dto_data["home_score"])
        self.assertEqual(tournament_dto.away_id, self.dto_data["away_id"])
        self.assertEqual(tournament_dto.away_score, self.dto_data["away_score"])

    def test_to_dict_property(self):
        # Test the to_dict property
        tournament_dto = TournamentDtoRequest(**self.dto_data)
        expected_dict = {
            "home_id": "home_team_id",
            "home_score": 2,
            "away_id": "away_team_id",
            "away_score": 1,
        }
        self.assertEqual(tournament_dto.to_dict, expected_dict)


class TournamentControllerTest(TestCase):
    def setUp(self):
        # Sample team data for testing
        self.home_team_data = {
            "id": str(uuid.uuid4()),
            "name": "Home Team",
        }
        self.away_team_data = {
            "id": str(uuid.uuid4()),
            "name": "Away Team",
        }
        Teams.objects.create(**self.home_team_data)
        Teams.objects.create(**self.away_team_data)

        # Sample tournament data for testing
        self.dto_data = {
            "home_id": self.home_team_data["id"],
            "home_score": 2,
            "away_id": self.away_team_data["id"],
            "away_score": 1,
        }
        self.dto_request = TournamentDtoRequest(**self.dto_data)

    def test_initialize_method(self):
        # Test the initialize method
        controller = TournamentController.initialize()
        self.assertIsInstance(controller, TournamentController)
        self.assertIsNone(controller.data)

    def test_from_payload_method(self):
        # Test the from_payload method
        controller = TournamentController.from_payload(self.dto_request)
        self.assertIsInstance(controller, TournamentController)
        self.assertEqual(controller.data, self.dto_request)

    def test_exists_method(self):
        # Test the exists method
        # Creating a sample record for testing
        sample_id = str(uuid.uuid4())
        Tournament.objects.create(
            id=sample_id,
            home_id=self.home_team_data["id"],
            away_id=self.away_team_data["id"],
        )
        self.assertTrue(TournamentController.exists(sample_id))
        self.assertFalse(TournamentController.exists(str(uuid.uuid4())))

    def test_list_method(self):
        # Test the list method
        # Creating a sample record for testing
        Tournament.objects.create(**self.dto_data)
        controller = TournamentController.initialize()
        result = controller.list()
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 1)

    def test_store_method(self):
        # Test the store method
        with patch.object(
            Tournament.objects, "create", return_value=Mock(id="new_record_id")
        ):
            controller = TournamentController(self.dto_request)
            result = controller.store()
            self.assertEqual(result, "new_record_id")

    def test_update_method(self):
        # Test the update method
        # Creating a sample record for testing
        existing_record = Tournament.objects.create(
            id=str(uuid.uuid4()),
            home_id=self.home_team_data["id"],
            away_id=self.away_team_data["id"],
        )
        controller = TournamentController(self.dto_request)
        with patch.object(
            Tournament.objects,
            "get",
            return_value=Mock(save=lambda: None, id="updated_record_id"),
        ):
            result = controller.update(existing_record.id)
            self.assertEqual(result, "updated_record_id")

    def test_delete_method(self):
        # Test the delete method
        # Creating a sample record for testing
        existing_record = Tournament.objects.create(
            id=str(uuid.uuid4()),
            home_id=self.home_team_data["id"],
            away_id=self.away_team_data["id"],
        )
        with patch.object(
            Tournament.objects,
            "get",
            return_value=Mock(delete=lambda: None, id="deleted_record_id"),
        ):
            controller = TournamentController.initialize()
            result = controller.delete(existing_record.id)
            self.assertEqual(result, existing_record.id)
