from core.models.thread import Thread


class ChatCreationService():
    def __init__(self, user1, user2):
        self.user1 = user1
        self.user2 = user2
    
    def create_chat(self):
        """
        Checks if a chat already exists between
        the users, if it does, returns the same
        if not, it creates a chat between them
        """

        thread_id = Thread.objects.get_thread(
            self.user1.id,
            self.user2.id
        )

        if thread_id is not None:
            return thread_id
        
        user1_message = {
            'text': f'You can start conversing with {self.user2.username} now!',
            'visibleTo': [self.user1.id]
        }
        user2_message = {
            'text': f'You can start conversing with {self.user1.username} now!',
            'visibleTo': [self.user2.id]
        }

        thread_id = Thread.objects.create_chat(
            self.user1.id,
            self.user2.id,
            message_list=[user1_message, user2_message]            
        )

        return thread_id
