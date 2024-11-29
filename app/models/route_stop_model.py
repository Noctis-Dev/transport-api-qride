from app.schemas.route_stop_schema import RouteStopRequest

class RouteStop:
    def __init__(self, id, name, stop_id, reference, routes, latitud, longitud):
        self.id = id
        self.name = name
        self.stop_id = stop_id
        self.reference = reference
        self.routes = routes
        self.latitud = latitud
        self.longitud = longitud



    def to_dict(self):
        return {
            "name": self.name,
            "stop_id": self.stop_id,
            "reference": self.reference,
            "routes": self.routes,
            "latitud": self.latitud,
            "longitud": self.longitud
        }

    @staticmethod
    def from_dict(id, source):
        return RouteStop(
            id,
            source["name"],
            source["stop_id"],
            source["reference"],
            source["routes"],
            source["latitud"],
            source["longitud"]
        )
    @staticmethod
    def from_request(request: RouteStopRequest, stop_id):
        return RouteStop(
            None,
            request.name,
            stop_id,
            request.reference,
            request.route,
            request.stop.latitude,
            request.stop.longitude
        )
        