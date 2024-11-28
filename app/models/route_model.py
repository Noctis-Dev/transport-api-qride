from app.schemas.route_schema import RouteRequest

class Route:
    def __init__(self, id, name, city_id, stops):
        self.id = id
        self.name = name
        self.city_id = city_id
        self.stops = stops

    def to_dict(self):
        return {
            "name": self.name,
            "city_id": self.city_id,
            "stops": self.stops
        }

    @staticmethod
    def from_dict(id, source):
        return Route(
            id,
            source["name"],
            source["city_id"],
            source["stops"]
        )
        
    @staticmethod
    def from_request(request: RouteRequest, stops):
        return Route(
            None,
            request.name,
            request.city_id,
            stops
        )