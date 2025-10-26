from unittest.mock import patch
from django.test import TestCase
from apps.users.services import get_all_users, get_all_invited_users


class GetAllUsersTest(TestCase):
    @patch("apps.users.services.User.objects")
    def test_get_all_users_calls_all(self, mock_objects):
        mock_queryset = mock_objects.all.return_value

        result = get_all_users()

        mock_objects.all.assert_called_once()
        self.assertEqual(result, mock_queryset)
    
    @patch("apps.users.services.InvitedUser.objects")
    def test_get_all_invited_users_calls_all(self, mock_objects):
        mock_queryset = mock_objects.all.return_value

        result = get_all_invited_users()

        mock_objects.all.assert_called_once()
        self.assertEqual(result, mock_queryset)
