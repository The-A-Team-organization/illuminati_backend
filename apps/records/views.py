from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import RecordSerializer
from .services import get_all_records, create_record
import os
import uuid
from django.conf import settings

from apps.records import serializers


class RecordListView(APIView):
    def get(self, request):
        records = get_all_records()
        serializer = RecordSerializer(records, many=True)

        return Response(
            {"status": "OK", "notification": "All records", "data": serializer.data},
            status=status.HTTP_200_OK,
        )


class RecordCreateView(APIView):
    def post(self, request):
        serializer = RecordSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {
                    "status": "ERROR",
                    "notification": "Invalid data",
                    "errors": serializer.errors,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        img = request.FILES.get("img")
        if not img:
            return Response(
                {"status": "ERROR", "notification": "Image is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        image_dir = os.path.join(settings.BASE_DIR, "shared", "images")
        os.makedirs(image_dir, exist_ok=True)

        ext = os.path.splitext(img.name)[1]
        unique_name = f"{uuid.uuid4().hex}{ext}"
        image_path = os.path.join(image_dir, unique_name)

        with open(image_path, "wb+") as dest:
            for chunk in img.chunks():
                dest.write(chunk)

        record_data = serializer.validated_data
        record_data["img_path"] = f"/images/{unique_name}"

        record_data["description"] = record_data.get(
            "description") or "No description"
        record_data["additional_info"] = record_data.get(
            "additional_info") or "N/A"

        record = create_record(record_data)

        return Response(
            {
                "status": "OK",
                "notification": "Record created successfully",
                "data": RecordSerializer(record).data,
            },
            status=status.HTTP_201_CREATED,
        )
