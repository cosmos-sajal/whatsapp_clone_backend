from celery.decorators import task
from celery.utils.log import get_task_logger
from django.core.mail import send_mail
from django.template.loader import render_to_string

from user.v1.services.email_verification_service \
    import EmailVerificationService
from core.models.user import User
from worker.worker import app

logger = get_task_logger(__name__)

def get_html_content(verification_link):
    return render_to_string(
        'user/verification_emailer.html',
        {'verification_link': verification_link}
    )

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

    verification_service = EmailVerificationService(user.id)
    verification_link = verification_service.get_verification_link()

    send_mail(
        "Email Verification Required",
        '',
        'sajal.4591@gmail.com',
        [user.email],
        fail_silently=False,
        html_message=get_html_content(verification_link)
    )

    return True
