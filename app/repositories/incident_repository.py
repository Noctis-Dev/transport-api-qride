from app.models.incident_model import Incident

class IncidentRepository:
    def __init__(self, db):
        self.db = db
    
    def save_incident(self, incident: Incident):
        incident_ref = self.db.collection('incidents').document()
        incident_ref.set(incident.to_dict())
        return incident_ref.id

    def get_incident(self, incident_id):
        incident_ref = self.db.collection('incidents').document(incident_id)
        incident = incident_ref.get()
        return Incident.from_dict(incident.id, incident.to_dict())
    
    def list_incidents(self):
        incidents = self.db.collection('incidents').stream()
        return [Incident.from_dict(incident.id, incident.to_dict()) for incident in incidents]