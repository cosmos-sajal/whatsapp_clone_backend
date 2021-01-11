from rest_framework import serializers

from core.models.user import User


class GenerateOTPSerializer(serializers.Serializer):
    mobile_number = serializers.CharField(required=True, max_length=15)

    def validate_mobile_number(self, mobile_number):
        if not User.objects.does_user_exist(mobile_number=mobile_number):
            raise serializers.ValidationError({
                'mobile_number': 'User does not exist'
            })
        
        return mobile_number
