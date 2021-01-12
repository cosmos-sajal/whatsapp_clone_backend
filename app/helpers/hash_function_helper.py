import hashlib
import hmac

from django.conf import settings


class HMACHelper():
    def __init__(self):
        self.SECRET_KEY = settings.SECRET_KEY

    def generate_hash(self, message):
        """
        Generate hash using hmac
        to be used in the parameters
        """

        return hmac.new(
            bytes(self.SECRET_KEY, 'utf-8'),
            bytes(message, 'utf-8'),
            hashlib.sha256
        ).hexdigest()
