from fastapi import APIRouter, Depends
from app.services.vehicle_service import VehicleService
from app.schemas.vehicle_schema import VehicleCreate, Vehicle
from app.db import get_db

router = APIRouter()


@router.post("/vehicles/", response_model=Vehicle)
def create_vehicle(vehicle: VehicleCreate, db: any = Depends(get_db)):
    vehicle_service = VehicleService(db)
    return vehicle_service.create_vehicle(vehicle)
