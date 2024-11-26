from app.models.city_model import City

class CityRepository:
    def __init__(self, db):
        self.db = db

    def save_city(self, city: City):
        city_ref = self.db.collection('cities').document()  # Sin especificar un ID
        city_ref.set(city.to_dict())
        return city_ref.id 