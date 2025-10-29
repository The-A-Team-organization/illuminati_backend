from rest_framework import serializers
from .models import Record


class RecordSerializer(serializers.ModelSerializer):
    img_path = serializers.CharField(read_only=True)
    description = serializers.CharField(required=False, allow_blank=True)
    additional_info = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = Record
        fields = [
            "id",
            "name",
            "x",
            "y",
            "type",
            "description",
            "img_path",
            "additional_info",
        ]

    def __init__(self, *args, **kwargs):
        fields = kwargs.pop("fields", None)
        super().__init__(*args, **kwargs)

        if fields is not None:
            allowed = set(fields)
            existing = set(self.fields)

            for field_name in existing - allowed:
                self.fields.pop(field_name)
