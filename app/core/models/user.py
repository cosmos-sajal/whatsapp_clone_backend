from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager,
                                        PermissionsMixin)
from django.core.exceptions import ObjectDoesNotExist
from django.db import models

from .base import BaseModel


class UserManager(BaseUserManager):
    def create_user(self, mobile_number, **extra_attributes):
        """
        Creates a saves a new user
        """
        if not mobile_number:
            raise ValueError('User should have a mobile_number')
        user = self.model(
            mobile_number=mobile_number,
            **extra_attributes)
        user.save(using=self._db)

        return user
    
    def does_user_exist(self, **kwargs):
        try:
            self.get(
                **kwargs,
                is_deleted=False
            )

            return True
        except ObjectDoesNotExist:
            return False
    
    def verify_email(self, user_id):
        self.filter(
            id=user_id,
            is_deleted=False
        ).update(
            is_email_verified=True
        )


class User(AbstractBaseUser, PermissionsMixin, BaseModel):
    """
    Custom user model
    """
    class Meta:
        db_table = 'users'
        indexes = [
            models.Index(fields=['mobile_number']),
        ]

    mobile_number = models.CharField(max_length=15, null=False)
    username = models.CharField(max_length=20, null=False)
    avatar = models.CharField(max_length=100, null=True)
    email = models.EmailField(max_length=255, null=False)
    is_email_verified = models.BooleanField(default=False)
    password, groups, user_permissions, is_superuser = None, None, None, None

    objects = UserManager()

    USERNAME_FIELD = 'id'

    def __str__(self):
        return str(self.id)
