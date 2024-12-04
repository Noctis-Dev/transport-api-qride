from fastapi import APIRouter, Depends, HTTPException
from app.db import get_firestore_db
from app.schemas.route_stop_schema import RouteStopRequest
from app.services.route_stop_service import RouteStopService
from app.schemas.base_response import BaseResponse
from app.schemas.route_stop_schema import NearbyStopsRequest as NearbyRouteStopsRequest
import logging

router = APIRouter()

@router.post("/route_stop", response_model=BaseResponse)
def create_route_stop(route_stop: RouteStopRequest, db=Depends(get_firestore_db)):
    try:
        logging.info(f"Creating route stop: {route_stop}")
        route_stop_service = RouteStopService(db)
        route_stop_response = route_stop_service.create_route_stop(route_stop)
        logging.info(f"Route stop created successfully: {route_stop_response}")
        return BaseResponse(data=route_stop_response, success=True, message="Se creo la parada")
    except Exception as e:
        logging.error(f"Error creating route stop: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/route_stops/nearby", response_model=BaseResponse)
def get_nearby_route_stops(latitude: str, longitude: str, radius: float, db=Depends(get_firestore_db)):
    try:
        logging.info(f"Fetching nearby route stops for latitude: {latitude}, longitude: {longitude}, radius: {radius}")
        request = NearbyRouteStopsRequest(latitude=latitude, longitude=longitude, radius=radius)
        route_stop_service = RouteStopService(db)
        nearby_route_stops = route_stop_service.get_nearby_route_stops(request)
        logging.info(f"Nearby route stops fetched successfully: {nearby_route_stops}")
        return BaseResponse(data=nearby_route_stops, success=True, message="Paradas cercanas")
    except Exception as e:
        logging.error(f"Error fetching nearby route stops: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))