import random

from datetime import datetime


def get_random_number(length=6):
    """
    Generate a random number of fixed length
    """
    numbers = "1234567890"

    return ''.join(random.choice(numbers) for i in range(length))


def get_created_at():
    return str(
        datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3]
        + 'Z'
    )
