from django.test import TestCase
from apps.entry_password.serializers import EntryPasswordSerializer

class TestEntryPasswordSerializer(TestCase):

    def test_create_with_password_passing(self):
        data = {"entry_password": "value1"}
        serializer = EntryPasswordSerializer(data = data)
        serializer.is_valid()
        data = serializer.data
        self.assertEqual(data["entry_password"], "value1")