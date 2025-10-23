from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .services import change_entry_password
from .serializers import EntryPasswordSerializer


class ChangeEntryView(APIView):
    def post(self, request):
        serializer = EntryPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        if not serializer.validated_data["password"]:
            return Response(
                {"status": "ERROR", "notification": "Missing password"},
                status=status.HTTP_400_BAD_REQUEST
            )

        change_entry_password(serializer.validated_data["password"])

        return Response(
            {"status": "OK", "notification": "Password changed!"},
            status=status.HTTP_200_OK
        )

       
