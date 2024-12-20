class Message: 
    def __init__(self, user, message, timestamp):
        self.user = user
        self.message = message
        self.timestamp = timestamp

    def to_dict(self):
        return {
            'user_id': self.user,
            'message': self.message,
            'timestamp': self.timestamp
        }