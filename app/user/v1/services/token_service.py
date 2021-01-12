import jwt
from django.conf import settings


class TokenService():
    def __init__(self):
        jwt_settings = settings.SIMPLE_JWT
        self.algorithm = jwt_settings['ALGORITHM']
        self.secret_key = jwt_settings['SIGNING_KEY']

    def __get_user(self, decoded_token):
        """
        Returns the user in the token
        """
        if 'user_id' in decoded_token:
            return decoded_token['user_id']
        else:
            return None

    def get_user_from_token(self, token):
        decoded_token = jwt.decode(
            token, self.secret_key,
            algorithms=[self.algorithm]
        )

        return self.__get_user(decoded_token)
