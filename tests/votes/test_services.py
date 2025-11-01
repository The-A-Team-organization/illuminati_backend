from unittest.mock import patch, MagicMock
from django.test import TestCase
from apps.votes.services import SendVoteService, VoteService, PermissionService,\
UserPromoteService, UserBanService
from datetime import date, datetime, timedelta
from enums.roles import Role
from enums.rules import VoteRules



class SendVoteServiceTest(TestCase):

    def setUp(self):
        self.user = MagicMock()
        self.user.id = 1
        self.user.role = "Mason"


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



class VoteServiceTest(TestCase):

    def setUp(self):
        self.user = MagicMock()
        self.user.id = 1
        self.user.role = "Mason"


    @patch("apps.votes.services.VoteService.get_vote_role_raw",
           return_value = ["PROMOTE_TO_SILVER"])
    @patch("apps.votes.services.connection.cursor")
    def test_get_all_votes(self, mock_cursor, mock_get_vote_role):
        mock_cursor_instance = MagicMock()
        mock_cursor.return_value.__enter__.return_value = mock_cursor_instance

        mock_cursor_instance.fetchall.return_value = [
            (1, "Promote John", "PROMOTE_TO_SILVER")
        ]

        service = VoteService(self.user)
        result = service.get_all_votes()

        self.assertEqual(result, [{"id": 1, "name": "Promote John", "vote_type": "PROMOTE_TO_SILVER"}])

        mock_cursor_instance.execute.assert_called()


    @patch("apps.votes.models.VoteTypes.objects")
    def test_get_vote_role_raw(self, mock_objects):
        mock_queryset = MagicMock()
        mock_queryset.values_list.return_value = ["PROMOTE_TO_SILVER", "BAN_USER"]
        mock_objects.filter.return_value = mock_queryset

        result = VoteService.get_vote_role_raw("SilverMason")
        self.assertEqual(result, ["PROMOTE_TO_SILVER", "BAN_USER"])

        mock_objects.filter.assert_called_once_with(user_role = "SilverMason")
        mock_queryset.values_list.assert_called_once_with("vote_type", flat = True)



class PermissionServiceTest(TestCase):

    def setUp(self):
        self.user = MagicMock()
        self.user.id = 10


    @patch("apps.votes.services.connection.cursor")
    @patch("apps.votes.services.date")
    def test_has_promote_permission_true(self, mock_date, mock_cursor):
        mock_cursor.return_value.__enter__.return_value.fetchall.return_value = [
            [date(2025, 1, 1), False]
        ]

        mock_date.today.return_value = date(2025, 1, 2)

        service = PermissionService(self.user)
        result = service.has_promote_permission()

        self.assertTrue(result)
        mock_cursor.assert_called_once()


    @patch("apps.votes.services.connection.cursor")
    @patch("apps.votes.services.date")
    def test_has_promote_permission_false(self, mock_date, mock_cursor):
        mock_cursor.return_value.__enter__.return_value.fetchall.return_value = [
            [date(2025, 1, 1), True]
        ]

        mock_date.today.return_value = date(2025, 1, 2)

        service = PermissionService(self.user)
        result = service.has_promote_permission()

        self.assertFalse(result)


    @patch("apps.votes.services.connection.cursor")
    def test_has_ban_permission_true(self, mock_cursor):
        mock_cursor.return_value.__enter__.return_value.fetchall.return_value = [(1,)]
        service = PermissionService(self.user)
        result = service.has_ban_permission()

        self.assertTrue(result)


    @patch("apps.votes.services.connection.cursor")
    def test_has_ban_permission_false(self, mock_cursor):
        mock_cursor.return_value.__enter__.return_value.fetchall.return_value = [(0,)]
        service = PermissionService(self.user)
        result = service.has_ban_permission()

        self.assertFalse(result)



class UserPromoteServiceTest(TestCase):

    def setUp(self):
        self.user = MagicMock()
        self.user.id = 10
        self.user.username = "test1"
        self.user.role = Role.MASON.value
        self.service = UserPromoteService(self.user)


    @patch("apps.votes.services.connection.cursor")
    @patch("apps.votes.services.datetime")
    def test_create_vote_success(self, mock_datetime, mock_cursor):
        fake_now = datetime(2025, 1, 1, 10, 0, 0)
        mock_datetime.now.return_value = fake_now
        mock_datetime.timedelta = timedelta
        mock_cursor.return_value.__enter__.return_value = MagicMock()

        result = self.service.create_vote()
        self.assertTrue(result)

        mock_cursor.assert_called_once()
        mock_datetime.now.assert_called_once()


    @patch("apps.votes.services.connection.cursor")
    def test_promote_user_success(self, mock_cursor):
        values = [
            {
                "count_of_agreed": 8,
                "count_of_disagreed": 2,
                "vote_type": VoteRules.rules.get(self.user.role),
                "user_id": self.user.id
            }
        ]

        date_of_promote = datetime(2025, 1, 2)
        mock_cursor.return_value.__enter__.return_value = MagicMock()
        res = UserPromoteService.promote_user(values, date_of_promote)

        self.assertTrue(res)
        self.assertTrue(mock_cursor.called)


    @patch("apps.votes.services.connection.cursor")
    def test_promote_user_not_enough_votes(self, mock_cursor):
        values = [
            {
                "count_of_agreed": 2,
                "count_of_disagreed": 8,
                "vote_type": VoteRules.rules.get(self.user.role),
                "user_id": self.user.id
            }
        ]

        date_of_promote = datetime(2025, 1, 2)
        mock_cursor.return_value.__enter__.return_value = MagicMock()
        res = UserPromoteService.promote_user(values, date_of_promote)

        self.assertTrue(res)

        mock_cursor.assert_not_called()



class UserBanServiceTest(TestCase):

    def setUp(self):
        self.service = UserBanService(user_id = 5, username = "test2")


    @patch("apps.votes.services.connection.cursor")
    @patch("apps.votes.services.datetime")
    def test_create_vote(self, mock_datetime, mock_cursor):
        fake_now = datetime(2025, 1, 1, 12, 0, 0)
        mock_datetime.now.return_value = fake_now
        mock_datetime.timedelta = timedelta

        mock_cursor.return_value.__enter__.return_value = MagicMock()

        result = self.service.create_vote()

        self.assertTrue(result)
        mock_cursor.assert_called_once()

        mock_datetime.now.assert_called_once()


    @patch("apps.votes.services.transaction.atomic")
    @patch("apps.votes.services.connection.cursor")
    def test_ban_user_success(self, mock_cursor, mock_atomic):
        values = [
            {
                "count_of_agreed": 8,
                "count_of_disagreed": 2,
                "user_id": 5
            }
        ]

        mock_cursor.return_value.__enter__.return_value = MagicMock()
        mock_atomic.return_value.__enter__.return_value = MagicMock()

        res = UserBanService.ban_user(values)

        self.assertTrue(res)
        self.assertTrue(mock_cursor.called)
        self.assertTrue(mock_atomic.called)


    @patch("apps.votes.services.transaction.atomic")
    @patch("apps.votes.services.connection.cursor")
    def test_ban_user_not_enough_votes(self, mock_cursor, mock_atomic):
        values = [
            {
                "count_of_agreed": 3,
                "count_of_disagreed": 7,
                "user_id": 5
            }
        ]

        mock_cursor.return_value.__enter__.return_value = MagicMock()
        mock_atomic.return_value.__enter__.return_value = MagicMock()

        res = UserBanService.ban_user(values)
        self.assertTrue(res)

        mock_cursor.assert_not_called()
        mock_atomic.assert_not_called()
