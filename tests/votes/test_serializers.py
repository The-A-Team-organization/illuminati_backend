from django.test import TestCase
from apps.votes.serializers import VotesSerializer, SendVotesSerializer
from apps.votes.models import Votes


class VotesSerializerTest(TestCase):

    def setUp(self):
        self.vote = Votes(
            id = 1,
            name = "Promote Vote 1",
            is_active = True,
            amount_of_agreed = 0,
            amount_of_disagreed = 0,
            user_in_question_id = 5,
            vote_type = "PROMOTE_TO_SILVER"
        )


    def test_serializer_serializes_all_fields(self):
        serializer = VotesSerializer(self.vote)
        data = serializer.data

        self.assertEqual(data["id"], 1)
        self.assertEqual(data["name"], "Promote Vote 1")
        self.assertEqual(data["vote_type"], "PROMOTE_TO_SILVER")


    def test_serializer_dynamic_fields(self):
        serializer = VotesSerializer(self.vote, fields = ["id", "name"])
        data = serializer.data

        self.assertEqual(set(data.keys()), {"id", "name"})



class SendVotesSerializerTest(TestCase):

    def test_serializer_valid_data(self):
        data = {"id": 1, "choice": "AGREE"}
        serializer = SendVotesSerializer(data = data)

        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.validated_data["id"], 1)
        self.assertEqual(serializer.validated_data["choice"], "AGREE")
