from pydantic import BaseModel

class RouteStopRequest(BaseModel):
    name: str
    stop_id: str
    reference: str

class RouteStopResponse(BaseModel):
    message: str
    stop_id: str
    route_id: str
