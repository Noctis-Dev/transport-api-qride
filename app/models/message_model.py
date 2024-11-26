class Message: 
    def __init__(self, user, message):
        self.user = user
        self.message = message

    def to_dict(self):
        return {
            'user_id': self.user,
            'message': self.message,
        }