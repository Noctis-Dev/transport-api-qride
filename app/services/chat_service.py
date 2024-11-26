from app.models.message_model import Message
from app.models.probable_incident_model import ProbableIncident
import time

KEYWORDS = ["peligro", "choque", "problema", "retardo"]

class ChatService:
    def __init__(self, db):
        self.db = db

    def send_message(self, route_name, user, message_content):
        timestamp = int(time.time())
        message = Message(user=user, message=message_content, timestamp=timestamp)
        messages_ref = self.db.child('chats').child(route_name).child('messages')
        new_message_ref = messages_ref.push()
        new_message_ref.set(message.to_dict())
        return new_message_ref.key
    
    @staticmethod
    def detect_keywords(message):
        return any(keyword in message.lower() for keyword in KEYWORDS)

    def create_incident(self, user, message):
        timestamp = int(time.time())
        incident = ProbableIncident(user=user, message=message, timestamp=timestamp)
        incidents_ref = self.db.child('incidents_probables')
        new_incident_ref = incidents_ref.push()
        new_incident_ref.set(incident.to_dict())
        return new_incident_ref.key


