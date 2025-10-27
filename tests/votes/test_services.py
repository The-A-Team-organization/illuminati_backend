from unittest.mock import patch, MagicMock
from django.test import TestCase
from apps.votes.services import VoteTableService, SendVoteService


class VoteTableServiceTest(TestCase):

    def setUp(self):
        self.user = MagicMock()
        self.user.id = 1
        self.user.role = "Mason"


    @patch("apps.votes.services.VoteTableService._VoteTableService__get_vote_role_raw",
           return_value = ["PROMOTE_TO_SILVER"])
    @patch("apps.votes.services.connection.cursor")
    def test_get_all_votes(self, mock_cursor, mock_get_vote_role):
        mock_cursor_instance = MagicMock()
        mock_cursor.return_value.__enter__.return_value = mock_cursor_instance

        mock_cursor_instance.fetchall.return_value = [
            (1, "Promote John", "PROMOTE_TO_SILVER")
        ]

        service = VoteTableService(self.user)
        result = service.get_all_votes()

        self.assertEqual(result, [{"id": 1, "name": "Promote John", "vote_type": "PROMOTE_TO_SILVER"}])

        mock_cursor_instance.execute.assert_called()



class SendVoteServiceTest(TestCase):

    @patch("apps.votes.services.connection.cursor")
    def test_user_already_voted_true(self, mock_cursor):
        mock_cursor_instance = MagicMock()
        mock_cursor.return_value.__enter__.return_value = mock_cursor_instance
        mock_cursor_instance.fetchall.return_value = [(True,)]

        service = SendVoteService()

        self.assertTrue(service.user_already_voted(1, 2))
        mock_cursor_instance.execute.assert_called()


    @patch("apps.votes.services.connection.cursor")
    def test_user_already_voted_false(self, mock_cursor):
        mock_cursor_instance = MagicMock()
        mock_cursor.return_value.__enter__.return_value = mock_cursor_instance
        mock_cursor_instance.fetchall.return_value = []

        service = SendVoteService()

        self.assertFalse(service.user_already_voted(1, 2))
        mock_cursor_instance.execute.assert_called()


    @patch("apps.votes.services.connection.cursor")
    def test_commit_choice_agree(self, mock_cursor):
        mock_cursor_instance = MagicMock()
        mock_cursor.return_value.__enter__.return_value = mock_cursor_instance

        service = SendVoteService()
        result = service.commit_choice(1, 2, "AGREE")

        self.assertTrue(result)
        mock_cursor_instance.execute.assert_called()


    @patch("apps.votes.services.connection.cursor")
    def test_commit_choice_disagree(self, mock_cursor):
        mock_cursor_instance = MagicMock()
        mock_cursor.return_value.__enter__.return_value = mock_cursor_instance

        service = SendVoteService()
        result = service.commit_choice(1, 2, "DISAGREE")

        self.assertTrue(result)
        mock_cursor_instance.execute.assert_called()


    def test_commit_choice_invalid(self):
        service = SendVoteService()
        result = service.commit_choice(1, 2, "INVALID")

        self.assertFalse(result)
