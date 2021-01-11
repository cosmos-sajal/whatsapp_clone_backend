from django.core.mail import send_mail
from celery.decorators import task
from celery.utils.log import get_task_logger
from worker.worker import app

from core.models.user import User

logger = get_task_logger(__name__)


@task(queue='send_verification_email')
def send_verification_email(user_id):
    """
    Sends the verification email to the user

    Args:
        user_id (int)
    """

    logger.info(
        "send_verification_email - user_id" +
        str(user_id)
    )

    user = User.objects.get(
        id=user_id,
        is_deleted=False
    )

    send_mail(
        "Welcome!",
        "Welcome to WhatsApp " + user.username,
        'sajal.4591@gmail.com',
        [user.email],
        fail_silently=False
    )

    return True
