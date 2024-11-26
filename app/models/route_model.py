class Route:
    def __init__(self, id, name, city_id):
        self.id = id
        self.name = name
        self.city_id = city_id

    def to_dict(self):
        return {
            "name": self.name,
            "city_id": self.city_id
        }

    @staticmethod
    def from_dict(id, source):
        return Route(
            id,
            source["name"],
            source["city_id"]
        )