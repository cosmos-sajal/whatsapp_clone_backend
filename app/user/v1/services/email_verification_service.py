from django.conf import settings
from django.urls import reverse

from core.models.user import User
from helpers.hash_function_helper import HMACHelper


class EmailVerificationService():
    BASE_URL = settings.REPO_BASE_URL
    ENDPOINT = 'api/v1/user/email/verify/'
    
    def __init__(self, user_id):
        self.user = User.objects.get(
            id=user_id,
            is_deleted=False
        )
        self.hash_helper = HMACHelper()
    
    def __get_hash_message(self):
        return str(self.user.uuid) + self.user.email
    
    def generate_hash(self):
        """
        Returns a hash message which
        will be used as a signature
        """

        hash_message = self.__get_hash_message()

        return self.hash_helper.generate_hash(hash_message)
    
    def get_verification_link(self):
        """
        Generates a verification link
        to be sent via email
        """

        hash_message = self.generate_hash()

        return self.BASE_URL + self.ENDPOINT + \
            '?user_id=' + str(self.user.id) + \
            '&signature=' + str(hash_message)
    
    def is_hash_valid(self, hash_signature):
        """
        Returns boolean after checking if the generated
        hash value is equal to what we have gotten in
        the request
        Args:
            hash_signature (str)
        """

        hash_message = self.__get_hash_message()
        generated_hash = self.hash_helper.generate_hash(hash_message)

        return generated_hash == hash_signature
