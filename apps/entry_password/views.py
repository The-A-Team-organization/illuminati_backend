from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import RegisterSerializer, LoginSerializer
from .services import register_user, authenticate_user, get_entry_pass
from core.settings import base
from .passwords import check_password
from .services import save_new_entry_password


class EntryView(APIView):

    def post(self, request):

        save_new_entry_password()

        return Response(
            {"status": "OK", "notification": "Entry verified"},
            status = status.HTTP_200_OK
        )

