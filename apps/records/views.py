from rest_framework.exceptions import PermissionDenied
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import RecordSerializer
from .services import get_all_records


class RecordListView(APIView):
    def get(self, request):
        records = get_all_users()
        serializer = RecordSerializer(records, many=True)

        return Response(
            {"status": "OK", "notification": "All records", "data": serializer.data},
            status=status.HTTP_200_OK,
        )
