import time

import jwt
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import authentication, exceptions

from core.models.user import User


class TokenAuthentication(authentication.BaseAuthentication):
    """
    Custom Authentication class for the repo
    """

    def __init__(self):
        self.exception_message = 'Invalid authentication token'

    def raise_token_exception(self):
        """
        Raises exception with the given message (401)
        """

        raise exceptions.AuthenticationFailed(self.exception_message)

    def check_expiry(self, decoded_token):
        """
        Checks the expiry of the token,
        if expired, returns the appropirate message
        """
        if 'exp' in decoded_token:
            expiry_timestamp = decoded_token['exp']
            current_timestamp = time.time()
            if current_timestamp > expiry_timestamp:
                self.exception_message = 'Token expired'
                self.raise_token_exception()
        else:
            self.raise_token_exception()

    def check_type(self, decoded_token):
        """
        Checks if the token type is access,
        if not, throws an exception
        """

        if not ('token_type' in decoded_token and
                decoded_token['token_type'] == 'access'):
            self.exception_message = 'Wrong token type'
            self.raise_token_exception()

    def get_user(self, decoded_token):
        """
        Returns the user in the token
        """
        if 'user_id' in decoded_token:
            return decoded_token['user_id']
        else:
            self.raise_token_exception()

    def authenticate(self, request):
        """
        Authenticates the token
        """

        authentication_token = request.META.get('HTTP_AUTHORIZATION')
        if not authentication_token:
            self.exception_message = "No Token provided"
            self.raise_token_exception()

        split_authentication_token = authentication_token.split()
        if len(split_authentication_token) < 2 or \
                split_authentication_token[0] != 'Bearer':
            self.raise_token_exception()

        bearer_token = split_authentication_token[1]

        try:
            jwt_settings = settings.TOKEN_CONFIG
            decoded_token = jwt.decode(
                bearer_token, jwt_settings['SECRET_KEY'],
                algorithms=[jwt_settings['ALGORITHM']]
            )
            user_id = self.get_user(decoded_token)
            self.check_expiry(decoded_token)
            self.check_type(decoded_token)
        except BaseException:
            self.raise_token_exception()

        return (user_id, None)

    def authenticate_header(self, request):
        """
        Method overridden to send 401 instead of 403
        """
        return 'Bearer Token'

    @staticmethod
    def get_user_in_request(user_id):
        """
        Returns if the user exists in the system
        """

        try:
            user = User.objects.get(
                id=user_id,
                is_deleted=False
            )

            return user
        except AttributeError:
            return None
        except ObjectDoesNotExist:
            return None
