from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from core.models.user import User
from helpers.custom_token_serializer import CustomTokenObtainPairSerializer
from user.v1.serializers.otp_serializer import GenerateOTPSerializer, ValidateOTPSerializer
from user.v1.services.otp_service import OTPService
from worker.user.send_otp_email import send_otp_email


class OTPGenerateView(APIView):
    """
    This API is used to create User in the
    backend
    """

    def post(self, request):
        """
        API -> /api/v1/user/otp/generate/
        """

        serializer = GenerateOTPSerializer(data=request.data)
        if serializer.is_valid():
            otp_service = OTPService(serializer.validated_data['mobile_number'])
            one_time_password = otp_service.generate_otp()
            send_otp_email.delay(
                serializer.validated_data['mobile_number'],
                one_time_password
            )

            return Response({'result': 'done'}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OTPValidateView(APIView):
    """
    This API is used to validate the OTP
    for the user and provide them with the access tokens
    and refresh tokens
    """

    def __get_tokens(self, mobile_number):
        """
        Returns the pair of access and refresh token
        for the user

        Args:
            mobile_number (str)
        """

        try:
            user = User.objects.get(
                mobile_number=mobile_number,
                is_deleted=False
            )
            refresh = \
                CustomTokenObtainPairSerializer.get_token(user)

            return str(refresh.access_token), str(refresh)
        except ObjectDoesNotExist:
            return None, None

    def post(self, request):
        """
        API -> POST /api/v1/user/otp/validate/
        """

        serializer = ValidateOTPSerializer(data=request.data)
        if serializer.is_valid():
            mobile_number = serializer.validated_data['mobile_number']
            access_token, refresh_token = \
                self.__get_tokens(mobile_number)
            otp_service = OTPService(mobile_number)
            otp_service.clear_otp()
            
            if access_token is None:
                return Response({
                    'error': 'User does not exist'
                }, status=status.HTTP_404_NOT_FOUND)

            return Response({
                'access_token': access_token,
                'refresh_token': refresh_token
            }, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
