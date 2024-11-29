from pydantic import BaseModel
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


class NearbyStopsResponse(BaseModel):
    stops: RouteStopResponse

