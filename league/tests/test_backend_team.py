import uuid
from unittest.mock import patch, Mock

from django.test import TestCase

from league.backends import TeamsDtoRequest, TeamsController
from league.models import Teams


class TeamsDtoRequestTest(TestCase):
    def setUp(self):
        # Sample data for testing
        self.dto_data = {
            "name": "Team Name",
        }
        self.dto_request = TeamsDtoRequest(**self.dto_data)

    def test_from_payload_method(self):
        # Test the from_payload method
        dto = TeamsDtoRequest.from_payload(name="New Team")
        self.assertIsInstance(dto, TeamsDtoRequest)
        self.assertEqual(dto.name, "New Team")

    def test_to_dict_property(self):
        # Test the to_dict property
        self.assertEqual(self.dto_request.to_dict, self.dto_data)


class TeamsControllerTest(TestCase):
    def setUp(self):
        # Sample data for testing
        self.dto_data = {
            "name": "Team Name",
        }
        self.dto_request = TeamsDtoRequest(**self.dto_data)

    def test_initialize_method(self):
        # Test the initialize method
        controller = TeamsController.initialize()
        self.assertIsInstance(controller, TeamsController)
        self.assertIsNone(controller.data)

    def test_from_payload_method(self):
        # Test the from_payload method
        controller = TeamsController.from_payload(self.dto_request)
        self.assertIsInstance(controller, TeamsController)
        self.assertEqual(controller.data, self.dto_request)

    def test_exists_method(self):
        # Test the exists method
        # Creating a sample record for testing
        sample_id = str(uuid.uuid4())
        Teams.objects.create(id=sample_id, name="Existing Team")
        self.assertTrue(TeamsController.exists(sample_id))
        self.assertFalse(TeamsController.exists(str(uuid.uuid4())))

    def test_list_method(self):
        # Test the list method
        # Creating a sample record for testing
        Teams.objects.create(**self.dto_data)
        controller = TeamsController.initialize()
        result = controller.list()
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["name"], self.dto_data["name"])

    def test_store_method(self):
        # Test the store method
        with patch.object(
            Teams.objects, "create", return_value=Mock(id="new_record_id")
        ):
            controller = TeamsController(self.dto_request)
            result = controller.store()
            self.assertEqual(result, "new_record_id")

    def test_update_method(self):
        # Test the update method
        # Creating a sample record for testing
        existing_record = Teams.objects.create(
            id=str(uuid.uuid4()), name="Existing Team"
        )
        controller = TeamsController(self.dto_request)
        with patch.object(
            Teams.objects,
            "get",
            return_value=Mock(save=lambda: None, id="updated_record_id"),
        ):
            result = controller.update(existing_record.id)
            self.assertEqual(result, "updated_record_id")

    def test_delete_method(self):
        # Test the delete method
        # Creating a sample record for testing
        existing_record = Teams.objects.create(
            id=str(uuid.uuid4()), name="Existing Team"
        )
        controller = TeamsController.initialize()
        result = controller.delete(existing_record.id)
        self.assertEqual(result, existing_record.id)
