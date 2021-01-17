from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from helpers.token_authentication import TokenAuthentication
from chat.v1.serializers.chat_serializer import CreateChatSerializer
from chat.v1.services.chat_creation_service import ChatCreationService


class CreateChatView(APIView):
    """
    This API is used to create chat between two users
    The first user will be the one who is calling the API
    The second user will be the one with the given username
    """

    authentication_classes = (TokenAuthentication,)

    def post(self, request, username):
        """
        API -> /api/v1/chat/create/<username>/
        """

        user = TokenAuthentication.get_user_in_request(
            request.user
        )

        if user is None:
            return Response({
                'error': 'Forbidden'
            }, status=status.HTTP_403_FORBIDDEN)
        
        request_data = request.data
        request_data['username'] = username
        request_data['requester_username'] = user.username

        serializer = CreateChatSerializer(data=request_data)
        try:
            serializer.is_valid(raise_exception=True)
            service = ChatCreationService(
                user,
                serializer.validated_data['user']
            )
            thread_id = service.create_chat()

            return Response({'thread_id': thread_id}, status=status.HTTP_200_OK)
        except ObjectDoesNotExist as msg:
            return Response(msg.args[0], status=status.HTTP_404_NOT_FOUND)
