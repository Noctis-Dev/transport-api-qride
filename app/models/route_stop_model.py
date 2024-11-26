class RouteStop:
    def __init__(self, id, name, route_id, stop_id):
        self.id = id
        self.name = name
        self.route_id = route_id
        self.stop_id = stop_id

    def to_dict(self):
        return {
            "name": self.name,
            "route_id": self.route_id,
            "stop_id": self.stop_id
        }

    @staticmethod
    def from_dict(id, source):
        return RouteStop(
            id,
            source["name"],
            source["route_id"],
            source["stop_id"]
        )