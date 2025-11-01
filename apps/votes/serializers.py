from rest_framework import serializers
from .models import Votes, User


class VotesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Votes
        fields = ['id', 'name', 'vote_type']


    def __init__(self, *args, **kwargs):
        fields = kwargs.pop('fields', None)
        super().__init__(*args, **kwargs)

        if fields is not None:

            allowed = set(fields)
            existing = set(self.fields)

            for field_name in existing - allowed:
                self.fields.pop(field_name)



class SendVotesSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    choice = serializers.CharField()



class CloseVotesSerializer(serializers.Serializer):
    date_of_end = serializers.DateTimeField(
        input_formats=[
            "%Y-%m-%d %H:%M:%S",
            "%Y-%m-%dT%H:%M:%S%z",
            "%Y-%m-%dT%H:%M:%S",
        ],
        required = True
    )


class UserBanSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    username = serializers.CharField()

    class Meta:
        model = User
        fields = ['id', 'username']