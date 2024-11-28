from fastapi import APIRouter, Depends
from app.db import get_firestore_db
from app.schemas.route_schema import RouteRequest, RouteResponse
from app.schemas.base_response import BaseResponse
from app.services.route_service import RouteService


router = APIRouter()

@router.post("/route", response_model=BaseResponse)
def create_route(route: RouteRequest, db: any = Depends(get_firestore_db)):
    route_service = RouteService(db)
    route = route_service.create_route(route)
    return BaseResponse(data=route, message="Route created successfully", success=True)