from django.db import models

from .base import BaseModel


class ThreadParticipant(BaseModel):
    """
    thread_participants table
    """

    class Meta:
        db_table = 'thread_participants'

    thread = models.ForeignKey(
        'core.Thread',
        on_delete=models.CASCADE,
        related_name='thread_participants'
    )
    user = models.ForeignKey(
        'core.user',
        on_delete=models.CASCADE,
        related_name='thread_users'
    )
