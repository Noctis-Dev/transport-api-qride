from fastapi import APIRouter, Depends
from app.db import get_firestore_db
from app.schemas.route_stop_schema import RouteStopRequest
from app.services.route_stop_service import RouteStopService
from app.schemas.base_response import BaseResponse
from app.schemas.route_stop_schema import NearbyStopsRequest as NearbyRouteStopsRequest



router = APIRouter()

@router.post("/route_stop", response_model=BaseResponse)
def create_route_stop( route_stop: RouteStopRequest, db=Depends(get_firestore_db)):
    route_stop_service = RouteStopService(db)
    route_stop_response = route_stop_service.create_route_stop(route_stop)
    return BaseResponse(data=route_stop_response, success=True, message="Se creo la parada")

@router.get("/route_stops/nearby", response_model=BaseResponse)
def get_nearby_route_stops(latitude: str, longitude: str, radius: float, db=Depends(get_firestore_db)):
    request = NearbyRouteStopsRequest(latitude=latitude, longitude=longitude, radius=radius)
    route_stop_service = RouteStopService(db)
    nearby_route_stops = route_stop_service.get_nearby_route_stops(request)
    return BaseResponse(data=nearby_route_stops, success=True, message="Paradas cercanas")