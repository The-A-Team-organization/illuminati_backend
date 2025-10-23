from rest_framework import serializers

class EntryPasswordSerializer(serializers.Serializer):
    password = serializers.CharField()
