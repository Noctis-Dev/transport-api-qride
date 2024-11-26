from fastapi import APIRouter, Depends
from app.db import get_firestore_db
from app.schemas.city_schema import CityCreate, ResponseCity
from app.services.city_service import CityService

router = APIRouter()


@router.post("/city", response_model=ResponseCity)
def create_vehicle(city: CityCreate, db: any = Depends(get_firestore_db)):
    city_service = CityService(db)
    return city_service.create_city(city)