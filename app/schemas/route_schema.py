from pydantic import BaseModel
from typing import List, Optional
from app.schemas.stop_schema import Stop

class RouteRequest(BaseModel):
    name: str
    city_id: str
    stops: List[Stop]

class RouteResponse(BaseModel):
    id: str
    name: str
    city_id: str
    stops: List[str]

class RoutesResponse(BaseModel):
    routes: List[RouteResponse] 
    
class RouteDrawRequest(BaseModel):
    stops: List[str]

class RouteDrawResponse(BaseModel):
    stops: List[Stop]
