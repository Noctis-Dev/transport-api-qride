from typing import List
from pydantic import BaseModel
from enum import Enum

class Status(str, Enum):
    OPEN = "OPEN" 
    CLOSED = "CLOSED"
    
class IncidentBase(BaseModel):
    id: str
    description: str
    status: Status
    created_at: str
    vehicle_id: str

class IncidentRequest(BaseModel):
    description: str
    status: Status
    vehicle_id: str
    
class IncidentResponse(BaseModel):
    id: str
    crated_at: str
    
class IncidentGetResponse(BaseModel):
    id: str
    created_at: str
    description: str
    status: Status 
    vehicle_id: str

    
class IncidentListResponse(BaseModel):
    incidents: List[IncidentBase]


    
