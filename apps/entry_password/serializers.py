from rest_framework import serializers
from .models import EntryPassword
from datetime import datetime


# class EntryPasswordSerializer(serializers.ModelSerializer):
#
#     class Meta:
#         model = EntryPassword
#         fields = ['entry_password', 'last_updated']
#
#     def create(self, validated_data):
#         validated_data['last_updated'] = datetime.now().strftime("%d/%m/%Y %H:%M")
#         return super().create(validated_data)
#

class EntryPasswordSerializer(serializers.Serializer):
    entry_password = serializers.CharField()