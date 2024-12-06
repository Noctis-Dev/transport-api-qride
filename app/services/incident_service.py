import datetime
from app.models.incident_model import Incident
from app.repositories.incident_repository import IncidentRepository
from app.schemas.incident_schema import IncidentRequest, IncidentGetResponse, IncidentListResponse, IncidentResponse, IncidentBase
from app.schemas.base_response import BaseResponse

class IncidentService:
    def __init__(self, db):
        self.repository = IncidentRepository(db)
        
    def save_incident(self, incident_request: IncidentRequest):
        incident = Incident.from_request(incident_request)
        incident.created_at = datetime.datetime.now().isoformat()
        incident_id = self.repository.save_incident(incident)
        data = IncidentResponse(id=incident_id, crated_at=incident.created_at)
        return BaseResponse(data=data, message="Incident created successfully", success=True, error='')
    
    def get_incident(self, incident_id):
        incident = self.repository.get_incident(incident_id)
        data = IncidentGetResponse( created_at=incident.created_at, description=incident.description, status=incident.status, vehicle_id=incident.vehicle_id, id=incident.id)
        return BaseResponse(data=data, message="Incident retrieved successfully", success=True, error='')
        
        
    def list_incidents(self):
        incidents = self.repository.list_incidents()
        base_incidents = []
        for incident in incidents:
            base_incident = IncidentBase(id=incident.id, description=incident.description, status=incident.status, vehicle_id=incident.vehicle_id, created_at=incident.created_at)
            base_incidents.append(base_incident)
        data = IncidentListResponse(incidents=base_incidents)
        return BaseResponse(data=data, message="Incidents retrieved successfully", success=True, error='')