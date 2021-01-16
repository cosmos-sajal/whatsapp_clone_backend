from firebase_admin import firestore


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

        message = "Welcome to Support, message here" + \
            " for help related to the product."

        user_ids = []
        for user in user_list:
            user_ids.append(user['id'])

        chat_ref = self.thread_ref.document(str(thread_id))
        chat_ref.set({
            u'users': user_ids,
            u'status': status
        })
        chat_ref.update({
            u'messages': firestore.ArrayUnion([{'text': message, 'system': True}])
        })

        user_chat_dict = {
            str(user_list[0]['id']) + '/chats/' + str(thread_id): {
                'username': user_list[1]['username'],
                'lastMessage': message,
                'threadId': thread_id,
                'avatar': user_list[1]['avatar'],
                'unreadCount': 1
            },
            str(user_list[1]['id']) + '/chats/' + str(thread_id): {
                'username': user_list[0]['username'],
                'lastMessage': message,
                'threadId': thread_id,
                'avatar': user_list[0]['avatar'],
                'unreadCount': 1
            }
        }

        for key, value in user_chat_dict.items():
            self.user_ref.document(key).set(value)
