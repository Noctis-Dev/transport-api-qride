from app.models.message_model import Message


class ChatService:
    def __init__(self, db):
        self.db = db

    def send_message(self, route_name, user, message_content):
        message = Message(user=user, message=message_content)
        messages_ref = self.db.child('chats').child(route_name).child('messages')
        new_message_ref = messages_ref.push()
        new_message_ref.set(message.to_dict())
        return new_message_ref.key


