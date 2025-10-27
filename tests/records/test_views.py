from unittest.mock import patch, MagicMock
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from io import BytesIO
from django.conf import settings
import tempfile


class RecordListViewTest(APITestCase):
    @patch("apps.records.views.get_all_records")
    def test_get_records_success(self, mock_get_all_records):
        mock_get_all_records.return_value = [
            type(
                "Record",
                (),
                {
                    "id": 1,
                    "name": "R1",
                    "x": 1.0,
                    "y": 2.0,
                    "type": "UFO",
                    "description": "desc",
                    "img_path": "/img.png",
                    "additional_info": "info",
                },
            )()
        ]

        url = reverse("records-all")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["status"], "OK")
        self.assertEqual(len(response.data["data"]), 1)


class RecordCreateViewTest(APITestCase):
    @patch("apps.records.views.create_record")
    def test_create_record_success(self, mock_create_record):
        settings.BASE_DIR = tempfile.gettempdir()

        mock_record = MagicMock()
        mock_record.id = 1
        mock_record.name = "R1"
        mock_record.x = 1.0
        mock_record.y = 2.0
        mock_record.type = "UFO"
        mock_record.description = "desc"
        mock_record.img_path = "/images/test.png"
        mock_record.additional_info = "info"
        mock_create_record.return_value = mock_record

        img = BytesIO(b"fake image data")
        img.name = "test.png"

        url = reverse("records-create")
        data = {
            "name": "R1",
            "x": 1.0,
            "y": 2.0,
            "type": "UFO",
            "description": "desc",
            "additional_info": "info",
            "img": img,
        }

        response = self.client.post(url, data, format="multipart")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["status"], "OK")
        self.assertEqual(response.data["notification"], "Record created successfully")
        mock_create_record.assert_called_once()

    def test_create_record_missing_image(self):
        settings.BASE_DIR = tempfile.gettempdir()

        url = reverse("records-create")
        data = {
            "name": "R1",
            "x": 1.0,
            "y": 2.0,
            "type": "UFO",
            "description": "desc",
        }

        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Invalid", str(response.data))

    def test_create_record_invalid_data(self):
        settings.BASE_DIR = tempfile.gettempdir()

        url = reverse("records-create")
        data = {"name": ""}

        response = self.client.post(url, data)

        self.assertEqual(response.data["status"], "ERROR")
        self.assertIn("Invalid data", response.data["notification"])
