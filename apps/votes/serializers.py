from rest_framework import serializers
from .models import Votes


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