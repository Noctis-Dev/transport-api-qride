import random
import string
from fastapi import HTTPException
import requests
import json
import time
from app.models.message_model import Message
from app.models.probable_incident_model import ProbableIncident
from app.auth import get_access_token

KEYWORDS = ["peligro ", "choque ", "problema ", "retardo "]
API_ENDPOINT = 'https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent'

class ChatService:
    def __init__(self, db):
        self.db = db

    def generate_message_key(self):
        return ''.join(random.choices(string.ascii_letters + string.digits, k=20))

    def send_message(self, route_name, user, message_content):
        try:
            timestamp = int(time.time())
            message = Message(user=user, message=message_content, timestamp=timestamp)
            messages_ref = self.db.child('chats').child(route_name).child('messages')
            message_key = self.generate_message_key()
            messages_ref.child(message_key).set(message.to_dict())
            return message_key
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    
    def analyze_message(self, message: str) -> bool:
        token = get_access_token()
        api_endpoint = API_ENDPOINT
        message = message.lower()
        try:
            prompt = (
                f"Analiza el siguiente mensaje: '{message}'. "
                "Evalúa los sentimientos en una escala del 1 al 5 (enteros) y devuelve solo un JSON "
                "{'polaridad': valor}. No des explicaciones. "
                "Considera las palabras clave relacionadas con incidentes de tránsito como {KEYWORDS} etc., "
                "para influir en la polaridad. La escala es: 1 no es un incidente, 5 es un incidente claro."
            )
            
            headers = {
                'Authorization': f'Bearer {token}',
                'Content-Type': 'application/json'
            }
            payload = {"contents": [{"parts": [{"text": prompt}]}]}
            
            response = requests.post(api_endpoint, headers=headers, json=payload)
        
            
            if response.status_code == 200:
                data = response.json()
                text_content = data["candidates"][0]["content"]["parts"][0]["text"].strip()
                if text_content.startswith("```json") and text_content.endswith("```"):
                    text_content = text_content[7:-3].strip()
                try:
                    json_content = json.loads(text_content)
                    polaridad = json_content.get("polaridad", 3)
                                       
                    # Verificación adicional para asegurar que la polaridad esté en el rango esperado
                    if 1 <= polaridad <= 5:
                        return polaridad > 3.5
                    else:
                        
                        return False
                except (json.JSONDecodeError, KeyError):
                    return False
            else:
                return False
        except Exception as e:
            
            return False

    def create_incident(self, user, message):
        try:
            timestamp = int(time.time())
            incident = ProbableIncident(user=user, message=message, timestamp=timestamp)
            incidents_ref = self.db.child('incidents_probables')
            new_incident_ref = incidents_ref.push()
            new_incident_ref.set(incident.to_dict())
            return new_incident_ref.key
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))