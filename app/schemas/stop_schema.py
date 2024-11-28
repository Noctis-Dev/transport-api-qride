from pydantic import BaseModel

class StopRequest(BaseModel):
    name: str
    latitude: float
    longitude: float
    reference: str




class ResponseStop(BaseModel):
    id: str
    name: str
    latitude: float
    longitude: float
    reference: str