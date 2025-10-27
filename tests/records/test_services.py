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
