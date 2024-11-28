from pydantic import BaseModel
from typing import List

class Stop(BaseModel):
    latitude: float
    longitude: float

class RouteRequest(BaseModel):
    name: str
    city_id: str
    stops: List[Stop]

class RouteResponse(BaseModel):
    id: str
    name: str
    
