from rest_framework import serializers
from django.core.exceptions import ObjectDoesNotExist

from core.models.user import User


class CreateChatSerializer(serializers.Serializer):
    username = serializers.CharField(required=True, max_length=20)
    requester_username = serializers.CharField(required=True, max_length=20)

    def validate(self, attrs):
        username = attrs.get('username')
        requester_username = attrs.get('requester_username')

        if requester_username == username:
            raise serializers.ValidationError({
                'username': 'Can not create chat with self'
            })

        try:
            user = User.objects.get(
                username=username,
                is_deleted=False
            )

            attrs['user'] = user
        except ObjectDoesNotExist:
            raise ObjectDoesNotExist({
                'username': 'User does not exist'
            })
        
        return attrs
