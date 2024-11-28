from fastapi import APIRouter, Depends
from app.db import get_firestore_db
from app.schemas.route_stop_schema import RouteStopRequest, RouteStopResponse # Importa el esquema correcto
from app.services.route_stop_service import RouteStopService


router = APIRouter()

@router.post("/routes/{route_id}/stops", response_model=RouteStopResponse)
def create_route_stop(route_id: str, stop: RouteStopRequest, db=Depends(get_firestore_db)):
    route_stop_service = RouteStopService(db)
    return route_stop_service.create_route_stop(route_id, stop)

