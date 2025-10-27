from unittest.mock import patch, MagicMock
from django.test import TestCase, RequestFactory
from apps.votes.views import VotesTable, SendVote
from rest_framework import status


class VotesTableViewTest(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.user = MagicMock()
        self.user.id = 1
        self.user.role = "Mason"


    @patch("apps.votes.views.HasValidToken.has_permission", return_value = True)
    @patch("apps.votes.views.VoteTableService")
    def test_get_votes_table(self, mock_service, _):
        mock_service.return_value.get_all_votes.return_value = [
            {"id": 1,
             "name": "Vote1",
             "vote_type": "PROMOTE_TO_SILVER"
            }
        ]

        request = self.factory.get("/votes/")
        request.user = self.user
        view = VotesTable.as_view()
        response = view(request)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["status"], "OK")



class SendVoteViewTest(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.user = MagicMock()
        self.user.id = 1


    @patch("apps.votes.views.HasValidToken.has_permission", return_value = True)
    @patch("apps.votes.views.SendVoteService")
    def test_send_vote_already_voted(self, mock_service, _):
        mock_service.return_value.user_already_voted.return_value = True

        request = self.factory.post("/votes/send/",
                                    {"id": 1,
                                     "choice": "AGREE"
                                     },
                                    content_type="application/json")
        request.user = self.user
        view = SendVote.as_view()
        response = view(request)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["status"], "ALREADY_VOTED")
