from rest_framework import serializers

from core.models.user import User
from user.v1.services.otp_service import OTPService


class GenerateOTPSerializer(serializers.Serializer):
    mobile_number = serializers.CharField(required=True, max_length=15)

    def validate_mobile_number(self, mobile_number):
        if not User.objects.does_user_exist(mobile_number=mobile_number):
            raise serializers.ValidationError({
                'mobile_number': 'User does not exist'
            })
        
        return mobile_number


class ValidateOTPSerializer(serializers.Serializer):
    mobile_number = serializers.CharField(required=True, max_length=15)
    otp = serializers.CharField(required=True, max_length=10)

    def validate(self, attrs):
        mobile_number = attrs.get('mobile_number')
        otp = attrs.get('otp')

        if not User.objects.does_user_exist(mobile_number=mobile_number):
            raise serializers.ValidationError({
                'mobile_number': 'User does not exist'
            })

        otp_service = OTPService(mobile_number)
        generated_otp = otp_service.get_otp()

        if generated_otp != otp:
            raise serializers.ValidationError({
                'otp': 'Wrong OTP'
            })

        return attrs
