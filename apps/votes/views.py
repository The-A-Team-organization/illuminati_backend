from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from .permissions import HasValidToken
from .services import VoteTableService,SendVoteService, PermissionService
from .serializers import VotesSerializer, SendVotesSerializer


class VotesTable(APIView):
    permission_classes = [HasValidToken]

    def get(self, request):
        user = request.user
        votes = VoteTableService(user)

        serializer = VotesSerializer(votes.get_all_votes(), fields = ['id', 'name', 'vote_type'], many = True)


        return Response(
            {
                "status": "OK",
                "notification": "All votes",
                "data": serializer.data
            },
            status = status.HTTP_200_OK
        )


class SendVote(APIView):
    permission_classes = [HasValidToken]

    def post(self, request):

        user = request.user

        serializer = SendVotesSerializer(data = request.data)
        serializer.is_valid(raise_exception = True)

        send = SendVoteService()

        if send.user_already_voted(user_id = user.id, vote_id = serializer.validated_data["id"]):
            return Response(
                {
                    "status": "ALREADY_VOTED",
                    "notification": "User already voted",
                },
                status = status.HTTP_400_BAD_REQUEST
            )

        result = send.commit_choice(
            user.id,
            serializer.validated_data["id"],
            serializer.validated_data["choice"]
        )

        if result:

            return Response(
                {
                    "status": "OK",
                    "notification": f"{result}",
                },
                status = status.HTTP_200_OK
            )


        return Response(
            {
                "status": "HTTP_409_CONFLICT",
                "notification": "Invalid request",
            },
            status=status.HTTP_409_CONFLICT
        )



class PromotionPermission(APIView):
    permission_classes = [HasValidToken]

    def get(self, request):
        user = request.user
        service = PermissionService(user)

        if service.has_promote_permission():
            return Response(
                {
                    "status": "OK"
                },
                status = status.HTTP_200_OK
            )

        return Response(
            {
                "status": "REFUSED",
            },
            status = status.HTTP_403_FORBIDDEN
        )



class BanPermission(APIView):
    permission_classes = [HasValidToken]

    def get(self, request):
        user = request.user

        service = PermissionService(user)

        if service.has_ban_permission():
            return Response(
                {
                    "status": "OK"
                }
            )

        return Response(
            {
                "status": "REFUSED",
            },
            status = status.HTTP_403_FORBIDDEN
        )