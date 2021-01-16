from firebase.firestore_adapter import FirestoreAdapter

from core.models.user import User
from helpers.cache_adapter import CacheAdapter
from user.v1.constants import BACKEND_USER_KEY


class BackendUserHelper():
    def __init__(self):
        self.firestore_adapter = FirestoreAdapter()
        self.cache_adapter = CacheAdapter()
    
    def create_user(self):
        """
        1. Creates a default backend user
        in backend
        2. Creates the same in Firestore
        """

        user = User.objects.create_user(
            username='WhatsApp Support',
            avatar='https://cdn4.iconfinder.com/data/icons/helpdesk-support-business/128/2_Support_helpdesk_avatar_business-20_Support_helpdesk_avatar_business-18-512.png',
            mobile_number='9999999999',
            email='whatsapp@yopmail.com'
        )

        self.firestore_adapter.create_user(
            user.id,
            user.username,
            mobile_number=user.mobile_number,
            avatar=user.avatar
        )

        self.cache_adapter.set(BACKEND_USER_KEY, user.id)
