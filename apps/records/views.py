from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import RecordSerializer
from .services import (
    get_all_records,
    create_record,
    get_record_by_id,
    erase_all_records,
)
import os
import uuid
from django.conf import settings
import jwt
import requests


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
        record_data["img_path"] = request.build_absolute_uri(
            f"{settings.MEDIA_URL}{unique_name}"
        )

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


class RecordDetailView(APIView):
    def get(self, request, record_id):
        record = get_record_by_id(record_id)
        if not record:
            return Response(
                {"status": "ERROR", "notification": "Record not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = RecordSerializer(record)
        return Response(
            {"status": "OK", "notification": "Record details", "data": serializer.data},
            status=status.HTTP_200_OK,
        )


class RecordEraseView(APIView):
    def post(self, request):
        auth_header = request.headers.get("Authorization", "")
        if not auth_header.startswith("Bearer "):
            return Response(
                {"status": "ERROR", "notification": "Missing or invalid token"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        token = auth_header.split(" ")[1]

        try:
            payload = jwt.decode(
                token, settings.SECRET_KEY, algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            return Response(
                {"status": "ERROR", "notification": "Token expired"},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        except jwt.InvalidTokenError:
            return Response(
                {"status": "ERROR", "notification": "Invalid token"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        role = payload.get("role")

        if role not in {"GoldMason", "Architect"}:
            return Response(
                {"status": "ERROR", "notification": "Unauthorized"},
                status=status.HTTP_403_FORBIDDEN,
            )

        erase_all_records()

        try:
            requests.post("http://docker_go:8080/trigger", timeout=2)
        except Exception as e:
            print("Trigger failed:", e)

        return Response(
            {"status": "OK", "notification": "All records erased."},
            status=status.HTTP_200_OK,
        )
