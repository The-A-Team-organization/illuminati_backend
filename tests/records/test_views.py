from unittest.mock import patch
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


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
