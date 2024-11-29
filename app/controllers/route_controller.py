from fastapi import APIRouter, Depends
from app.db import get_firestore_db
from app.schemas.route_schema import RouteRequest, RouteResponse
from app.schemas.base_response import BaseResponse
from app.services.route_service import RouteService
from app.models.route_model import Route
from app.schemas.route_schema import RoutesResponse
from typing import List



router = APIRouter()

@router.post("/route", response_model=BaseResponse)
def create_route(route: RouteRequest, db: any = Depends(get_firestore_db)):
    route_service = RouteService(db)
    route = route_service.create_route(route)
    return BaseResponse(data=route, message="Route created successfully", success=True)

@router.get("/routes", response_model=BaseResponse)  
def get_all_routes(db: any = Depends(get_firestore_db)):
    route_service = RouteService(db)
    routes_data = route_service.get_all_routes()
    
    routes_response = []

    for route_data in routes_data :
        route = RouteResponse(id=route_data.id, name=route_data.name, city_id=route_data.city_id, stops=route_data.stops)
        routes_response.append(route)

    routes = RoutesResponse(routes=routes_response) 
    return BaseResponse(data=routes, message="Routes retrieved successfully", success=True)
    