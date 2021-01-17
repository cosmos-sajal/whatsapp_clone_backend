from firebase_admin import firestore

from helpers.misc_helper import get_created_at


class FirestoreAdapter():
    def __init__(self):
        db = firestore.client()
        self.user_ref = db.collection(u'users')
        self.thread_ref = db.collection(u'threads')
    
    def create_user(self, user_id, username, **kwargs):
        """
        Add user in Firestore.
        """

        mobile_number = kwargs.pop('mobile_number', None)
        avatar = kwargs.pop('avatar', None)

        ref = self.user_ref.document(str(user_id))
        ref.set({
            u'username': username,
            u'mobile_number': mobile_number,
            u'avatar': avatar
        })

    def create_chat(self, thread_id, user_list, **kwargs):
        """
        1. Creates a chat between the users
        2. Adds the chat and last messages

        Args:
            thread_id (int)
            user_list (list)
        """

        status = kwargs.pop('status', 'active')
        message_list = kwargs.pop('message_list', None)

        user_ids = []
        for user in user_list:
            user_ids.append(user['id'])

        chat_ref = self.thread_ref.document(str(thread_id))
        chat_ref.set({
            u'users': user_ids,
            u'status': status
        })

        if message_list is not None:
            chat_ref.update({
                u'messages': firestore.ArrayUnion(message_list)
            })

        created_at = get_created_at()
        user_chat_dict = {
            str(user_list[0]['id']) + '/chats/' + str(thread_id): {
                'username': user_list[1]['username'],
                'threadId': thread_id,
                'avatar': user_list[1]['avatar'],
                'updatedAt': created_at,
                'userId': user_list[1]['id']
            },
            str(user_list[1]['id']) + '/chats/' + str(thread_id): {
                'username': user_list[0]['username'],
                'threadId': thread_id,
                'avatar': user_list[0]['avatar'],
                'updatedAt': created_at,
                'userId': user_list[0]['id']
            }
        }

        for key, value in user_chat_dict.items():
            self.user_ref.document(key).set(value)
