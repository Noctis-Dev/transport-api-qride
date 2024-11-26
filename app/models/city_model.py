from app.schemas.city_schema import CityCreate

class City:
    def __init__(self, id, name):
        self.id = id
        self.name = name

    def to_dict(self):
        return {
            "name": self.name
        }

    @staticmethod
    def from_dict(id, source):
        return City(
            id=id,
            name=source["name"]
        )
        
    @staticmethod
    def from_create(city_create: CityCreate):
        return City(
            id=None,
            name=city_create.name
        )