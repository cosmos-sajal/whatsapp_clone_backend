from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from user.v1.serializers.otp_serializer import GenerateOTPSerializer
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
