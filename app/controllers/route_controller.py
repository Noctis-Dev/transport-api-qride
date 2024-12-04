from fastapi import APIRouter, Depends, HTTPException, Query
from app.db import get_firestore_db
from app.schemas.route_schema import RouteRequest, RouteResponse, RouteDrawRequest
from app.schemas.base_response import BaseResponse
from app.services.route_service import RouteService
from app.models.route_model import Route
from app.schemas.route_schema import RoutesResponse
from typing import List
import logging

router = APIRouter()

@router.post("/route", response_model=BaseResponse)
def create_route(route: RouteRequest, db: any = Depends(get_firestore_db)):
    try:
        logging.info(f"Creating route: {route}")
        route_service = RouteService(db)
        route = route_service.create_route(route)
        logging.info(f"Route created successfully: {route}")
        return BaseResponse(data=route, message="Route created successfully", success=True)
    except Exception as e:
        logging.error(f"Error creating route: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/routes", response_model=BaseResponse)
def get_all_routes(db: any = Depends(get_firestore_db)):
    try:
        logging.info("Fetching all routes")
        route_service = RouteService(db)
        routes_data = route_service.get_all_routes()
        
        routes_response = []

        for route_data in routes_data:
            route = RouteResponse(id=route_data.id, name=route_data.name, city_id=route_data.city_id, stops=route_data.stops)
            routes_response.append(route)

        routes = RoutesResponse(routes=routes_response)
        logging.info("Routes retrieved successfully")
        return BaseResponse(data=routes, message="Routes retrieved successfully", success=True)
    except Exception as e:
        logging.error(f"Error fetching routes: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/route/{route_id}", response_model=BaseResponse)
def get_route_draw(route_draw: RouteDrawRequest = Query(None), db: any = Depends(get_firestore_db)):
    try:
        logging.info(f"Fetching route draw for route_id: {route_draw.route_id}")
        route_service = RouteService(db)
        route = route_service.get_route_stops(route_draw)
        logging.info(f"Route retrieved successfully for route_id: {route_draw.route_id}")
        return BaseResponse(data=route, message="Route retrieved successfully", success=True)
    except Exception as e:
        logging.error(f"Error fetching route draw for route_id: {route_draw.route_id} - {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
    