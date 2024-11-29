from pydantic import BaseModel
from typing import List
from app.schemas.route_schema import Stop

class RouteStopRequest(BaseModel):
    name: str
    reference: str
    route: str
    stop: Stop


class RouteStopResponse(BaseModel):
    route_stop_id: str
    name: str 


class NearbyStopsRequest(BaseModel):
    latitude: float
    longitude: float
    radius: float = 5.0

class NearbyStops(RouteStopResponse):
    latitude: float
    longitude: float
    
class NearbyStopsResponse(BaseModel):
    stops: List[NearbyStops] = []

