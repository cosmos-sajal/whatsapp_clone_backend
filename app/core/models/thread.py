from django.core.exceptions import ObjectDoesNotExist
from django.db import models

from .base import BaseModel
from core.models.user import User
from core.models.thread_participant import ThreadParticipant
from firebase.firestore_adapter import FirestoreAdapter


class ThreadManager(models.Manager):
    def create_chat(self, user1_id, user2_id, **kwargs):
        """
        Creates a chat between the two users

        Arguments:
            user1_id {int}
            user2_id {int}
        """

        user1 = User.objects.get(
            id=user1_id,
            is_deleted=False
        )

        user2 = User.objects.get(
            id=user2_id,
            is_deleted=False
        )

        user_list = [
            {
                'id': user1.id,
                'username': user1.username,
                'avatar': user1.avatar
            },
            {
                'id': user2.id,
                'username': user2.username,
                'avatar': user2.avatar
            }
        ]

        # creating thread
        thread = self.create(
            status='active'
        )

        # creating thread participants
        ThreadParticipant.objects.create(
            thread=thread,
            user_id=user1_id
        )
        ThreadParticipant.objects.create(
            thread=thread,
            user_id=user2_id
        )

        # creating the chat in Firestore
        firestore_adapter = FirestoreAdapter()
        firestore_adapter.create_chat(thread.id, user_list, **kwargs)

        return thread.id
    
    def create_intro_chat(self, user_id):
        """
        Creates a chat with the backend user

        Args:
            user_id (int)
        """

        message = "Welcome to Support, message here" + \
                    " for help related to the product."
        backend_user = User.objects.get_backend_user()

        return self.create_chat(
            user_id,
            backend_user.id,
            message_list=[{'text': message, 'system': True}]
        )
    
    def get_thread(self, user1_id, user2_id):
        """
        Returns a thread if it exists between
        the users, returns none otherwise

        Arguments:
            user1_id {int}
            user2_id {int}
        """

        try:
            user1_threads = ThreadParticipant.objects.filter(
                user_id=user1_id,
                is_deleted=False
            ).values_list('thread_id')

            user2_threads = ThreadParticipant.objects.filter(
                user_id=user2_id,
                is_deleted=False
            ).values_list('thread_id')

            intersecting_threads = \
                list(set(user1_threads) & set(user2_threads))

            if len(intersecting_threads) != 0:
                return intersecting_threads[0][0]
            else:
                return None
        except ObjectDoesNotExist:
            return None
    
    def does_chat_exist(self, user1_id, user2_id):
        """
        Checks if a chat exist between the two users

        Args:
            user1_id (int)
            user2_id (int)
        """

        if self.get_thread(user1_id, user2_id) is None:
            return False
        else:
            return True


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
