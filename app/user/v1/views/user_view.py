from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from user.v1.serializers.user_serializer import RegisterUserSerializer


class RegisterUserView(APIView):
    """
    This API is used to create User in the
    backend
    """

    def post(self, request):
        """
        API -> /api/v1/user/register/
        """

        serializer = RegisterUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()

            return Response({'result': 'done'}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
