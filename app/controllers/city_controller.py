from fastapi import APIRouter, Depends
from app.db import get_db
from app.schemas.city_schema import CityCreate, CityResponse
from app.services.city_service import CityService

router = APIRouter()


@router.post("/city", response_model=CityResponse)
def create_vehicle(city: CityCreate, db: any = Depends(get_db)):
    city_service = CityService(db)
    return city_service.create_city(city)