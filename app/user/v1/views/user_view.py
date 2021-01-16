from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework_simplejwt.serializers import TokenRefreshSerializer

from core.models.user import User
from user.v1.services.token_service import TokenService
from user.v1.serializers.user_serializer import RegisterUserSerializer, SignatureHashSerializer
from worker.chat.onboard_user import onboard_user
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
            onboard_user.delay(user.id)

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


class RefreshTokenView(APIView):
    """
    This API is used to generate a new
    pair of refresh and access token
    using the refresh_token of a user
    """

    def post(self, request):
        """
        API -> POST /api/v1/user/refresh/token/
        """

        serializer = TokenRefreshSerializer(data=request.data)
        try:
            if serializer.is_valid():
                token_service = TokenService()
                user_id = token_service.get_user_from_token(
                    request.data['refresh']
                )

                if user_id is None:
                    return Response(
                        {'error': 'Invalid Claims'},
                        status=status.HTTP_401_UNAUTHORIZED
                    )
                
                try:
                    User.objects.get(
                        id=user_id,
                        is_deleted=False
                    )
                except ObjectDoesNotExist:
                    return Response(
                        {'error': 'User does not exist'},
                        status=status.HTTP_401_UNAUTHORIZED
                    )
                
                tokens = serializer.validated_data

                return Response({
                    'access_token': tokens['access'],
                    'refresh_token': tokens['refresh']
                }, status=status.HTTP_200_OK)
        except Exception as error:
            return Response({'error': str(error)},
                            status=status.HTTP_403_FORBIDDEN)
