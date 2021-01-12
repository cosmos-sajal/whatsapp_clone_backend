from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.renderers import TemplateHTMLRenderer

from core.models.user import User
from user.v1.serializers.user_serializer import RegisterUserSerializer, SignatureHashSerializer
from worker.user.send_verification_email import send_verification_email


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
            user = serializer.save()
            send_verification_email.delay(user.id)

            return Response({'result': 'done'}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyEmailView(APIView):
    """
    This API is used to verify Email
    using the verification link sent to the
    user on the email provided
    """

    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'user/email_verification.html'

    def get(self, request):
        """
        API -> GET /api/v1/user/email/verify/
        """

        serializer = SignatureHashSerializer(data=request.query_params)
        if serializer.is_valid():
            user_id = serializer.validated_data['user_id']
            User.objects.verify_email(user_id)

            return Response(
                {'is_success': True, 'message': 'Email Verified'}
            )

        return Response(
            {'is_success': False, 'error': 'Invalid Request'}
        )
