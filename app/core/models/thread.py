from django.db import models

from .base import BaseModel
from core.models.user import User
from core.models.thread_participant import ThreadParticipant
from firebase.firestore_adapter import FirestoreAdapter


class ThreadManager(models.Manager):
    def create_intro_chat(self, user_id):
        """
        Creates a chat with the backend user

        Args:
            user_id (int)
        """

        user = User.objects.get(
            id=user_id,
            is_deleted=False
        )
        backend_user = User.objects.get_backend_user()
        user_list = [
            {
                'id': user.id,
                'username': user.username,
                'avatar': user.avatar
            },
            {
                'id': backend_user.id,
                'username': backend_user.username,
                'avatar': backend_user.avatar
            }
        ]

        # creating thread
        thread = self.create(
            status='active'
        )

        # creating thread participants
        ThreadParticipant.objects.create(
            thread=thread,
            user_id=user_id
        )
        ThreadParticipant.objects.create(
            thread=thread,
            user_id=backend_user.id
        )

        # creating the chat in Firestore
        firestore_adapter = FirestoreAdapter()
        firestore_adapter.create_chat(thread.id, user_list)


class Thread(BaseModel):
    """
    Thread model
    """
    class Meta:
        db_table = 'threads'

    status = models.CharField(
        max_length=20,
        default='active'
    )

    objects = ThreadManager()
