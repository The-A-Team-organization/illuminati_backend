from django.test import TestCase
from apps.entry_password.services import get_new_entry_password
import httpretty

class GetNewEntryPassword(TestCase):

    @httpretty.activate(verbose=True, allow_net_connect=True)
    def test_get_new_entry_password(self):
        httpretty.register_uri(
            httpretty.GET,
            "https://docker_go:8080/new-word",
            body='{"entry_password": "value1"}'
        )
        json_data = get_new_entry_password()
        self.assertEqual(json_data, {"entry_password": "value1"})

