from django.core.mail import send_mail
from celery.decorators import task
from celery.utils.log import get_task_logger
from worker.worker import app

from core.models.user import User
from core.models.thread import Thread
from firebase.firestore_adapter import FirestoreAdapter

logger = get_task_logger(__name__)


@task(queue='onboard_user')
def onboard_user(user_id):
    """
    1. Creates user in firestore
    2. Creates a chat with Backend Support User

    Args:
        user_id (int)
    """

    logger.info(
        "onboard_user - user_id:" +
        str(user_id)
    )

    user = User.objects.get(
        id=user_id,
        is_deleted=False
    )
    firestore_adapter = FirestoreAdapter()
    firestore_adapter.create_user(
        user.id,
        user.username,
        mobile_number=user.mobile_number
    )

    logger.info(
        "onboard_user - user_id:" +
        str(user_id) +
        " creating intro chat"
    )
    Thread.objects.create_intro_chat(user_id)

    return True
