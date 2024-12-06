from app.schemas.incident_schema import IncidentRequest

class Incident: 
    def __init__(self, id, description, status, created_at, vehicle_id):
        self.id = id
        self.description = description
        self.status = status
        self.created_at = created_at
        self.vehicle_id = vehicle_id
    
    def to_dict(self):
        return {
            "description": self.description,
            "status": self.status,
            "created_at": self.created_at,
            "vehicle_id": self.vehicle_id
        }
        
    @staticmethod
    def from_dict(id, source):
        return Incident(
            id,
            source["description"],
            source["status"],
            source["created_at"],
            source["vehicle_id"]
        )
        
    @staticmethod
    def from_request(incident_request: IncidentRequest):
        return Incident(
            None,
            incident_request.description,
            incident_request.status,
            None,
            incident_request.vehicle_id
        )

    