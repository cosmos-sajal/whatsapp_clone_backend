from django.core.mail import send_mail
from celery.decorators import task
from celery.utils.log import get_task_logger
from worker.worker import app

from core.models.user import User

logger = get_task_logger(__name__)


@task(queue='send_otp_email')
def send_otp_email(mobile_number, otp):
    """
    Sends the OTP email to the user

    Args:
        mobile_number (str)
        otp (str)
    """

    logger.info(
        "send_otp_email - mobile_number:" +
        mobile_number
    )

    user = User.objects.get(
        mobile_number=mobile_number,
        is_deleted=False
    )

    send_mail(
        "OTP for Signing In!",
        "Your OTP for logging into the service is - " + otp,
        'sajal.4591@gmail.com',
        [user.email],
        fail_silently=False
    )

    return True
