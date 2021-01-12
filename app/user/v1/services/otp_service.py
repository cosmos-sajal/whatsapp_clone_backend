from helpers.cache_adapter import CacheAdapter
from helpers.misc_helper import get_random_number


class OTPService():
    def __init__(self, mobile_number):
        self.mobile_number = mobile_number
        self.OTP_PREFIX = 'OTP_'
        self.OTP_EXPIRY = 600 # in seconds
        self.cache_adapter = CacheAdapter()
    
    def get_otp(self):
        """
        Returns the OTP stored in cache for
        the given number
        """

        key = self.OTP_PREFIX + self.mobile_number

        return self.cache_adapter.get(key)
    
    def clear_otp(self):
        """
        Clears the OTP from the cache
        """

        key = self.OTP_PREFIX + self.mobile_number
        self.cache_adapter.delete(key)        
    
    def generate_otp(self):
        """
        Generates OTP for the given mobile number
        """

        key = self.OTP_PREFIX + self.mobile_number
        
        # Gets a new OTP if not present in cache,
        # and if it's already present, returns the same
        # OTP
        one_time_password = self.cache_adapter.get(key)
        if one_time_password is None:
            one_time_password = get_random_number()

        # setting the OTP in cache
        self.cache_adapter.set(
            key,
            one_time_password,
            self.OTP_EXPIRY
        )

        return one_time_password
