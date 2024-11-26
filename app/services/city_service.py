from app.repositories.city_repository import CityRepository
from app.models.city_model import City
from app.schemas.city_schema import CityCreate, ResponseCity


class CityService: 
    def __init__(self, db: any):
        self.city_repository = CityRepository(db)

    def create_city(self, city: CityCreate):
        city = City.from_create(city)
        city_id = self.city_repository.save_city(city)
        return ResponseCity(id=city_id)