from unittest.mock import patch
from django.test import TestCase
from apps.records.services import get_all_records


class GetAllRecordsTest(TestCase):
    @patch("apps.records.services.Record.objects")
    def test_get_all_records_calls_all(self, mock_objects):
        mock_queryset = mock_objects.all.return_value

        result = get_all_records()

        mock_objects.all.assert_called_once()
        self.assertEqual(result, mock_queryset)


class CreateRecordTest(TestCase):
    @patch("apps.records.services.Record.objects.create")
    def test_create_record_calls_create_with_data(self, mock_create):
        data = {
            "name": "New record",
            "x": 3.0,
            "y": 4.0,
            "type": "UFO",
            "description": "desc",
            "img_path": "/img.png",
            "additional_info": "info",
        }

        mock_record = mock_create.return_value
        from apps.records.services import create_record

        result = create_record(data)

        mock_create.assert_called_once_with(**data)
        self.assertEqual(result, mock_record)


class GetRecordByIdTest(TestCase):
    @patch("apps.records.services.Record.objects.get")
    def test_get_record_by_id_calls_get_with_correct_id(self, mock_get):
        mock_record = mock_get.return_value
        from apps.records.services import get_record_by_id

        result = get_record_by_id(5)

        mock_get.assert_called_once_with(id=5)
        self.assertEqual(result, mock_record)
