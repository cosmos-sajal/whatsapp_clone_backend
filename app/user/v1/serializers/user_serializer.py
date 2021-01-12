from rest_framework import serializers
from django.core.exceptions import ObjectDoesNotExist

from core.models.user import User
from helpers.validators import is_valid_email, \
    is_valid_mobile_number, is_valid_username
from user.v1.services.email_verification_service \
    import EmailVerificationService


class RegisterUserSerializer(serializers.Serializer):
    mobile_number = serializers.CharField(required=True, max_length=15)
    username = serializers.CharField(required=True, max_length=20)
    email = serializers.CharField(required=True, max_length=255)

    def validate_mobile_number(self, mobile_number):
        if not is_valid_mobile_number(mobile_number):
            raise serializers.ValidationError({
                'mobile_number': 'Not a valid mobile number'
            })
        
        if User.objects.does_user_exist(mobile_number=mobile_number):
            raise serializers.ValidationError({
                'mobile_number': 'User exists'
            })
        
        return mobile_number
    
    def validate_email(self, email):
        if not is_valid_email(email):
            raise serializers.ValidationError({
                'email': 'Not a valid email'
            })
        
        if User.objects.does_user_exist(email=email):
            raise serializers.ValidationError({
                'email': 'User exists'
            })
        
        return email

    def validate_username(self, username):
        if not is_valid_username(username):
            raise serializers.ValidationError({
                'username': 'Not a valid username'
            })
        
        if User.objects.does_user_exist(username=username):
            raise serializers.ValidationError({
                'username': 'User exists'
            })
        
        return username
    
    def create(self, validated_data):
        """
        Creates the user in core_user table
        """
        
        return User.objects.create_user(**validated_data)


class SignatureHashSerializer(serializers.Serializer):
    user_id = serializers.IntegerField(required=True)
    signature = serializers.CharField(required=True)

    def validate(self, attrs):
        """
        Checks if the request is valid or not
        """

        user_id = attrs.get('user_id')
        signature = attrs.get('signature')

        if not User.objects.does_user_exist(
            id=user_id
        ):
            raise serializers.ValidationError(
                "User does not exist"
            )

        service = EmailVerificationService(user_id)
        if not service.is_hash_valid(signature):
            raise serializers.ValidationError(
                "Invalid Request"
            )

        return attrs
