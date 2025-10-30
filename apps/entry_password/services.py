import requests, json
from .models import EntryPassword
from .serializers import EntryPasswordSerializer
from rest_framework.response import Response
from datetime import datetime

def get_new_entry_password():
    response = requests.get("https://docker_go:8080/new-word", timeout=2)
    payload = response.json()
    return payload


def save_new_entry_password(entry_password):
    old_password = EntryPassword.objects.filter().first()
    if not old_password:
        raise ValueError("Ups.. perhaps the is no any password in db saved")

    EntryPassword.objects.update(
        id=old_password.id ,entry_password=entry_password, last_updated=datetime.now().strftime("%d/%m/%Y %H:%M")
    )

    return old_password

def el_combinero():
    pyld = get_new_entry_password()
    serializer = EntryPasswordSerializer(data=pyld)
    serializer.is_valid(raise_exception=True)
    save_new_entry_password(
       serializer.validated_data["entry_password"]
    )
