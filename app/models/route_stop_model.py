class RouteStop:
    def __init__(self, id, name, stop_id, reference):
        self.id = id
        self.name = name
        self.stop_id = stop_id
        self.reference = reference

    def to_dict(self):
        return {
            "name": self.name,
            "route_id": self.route_id,
            "stop_id": self.stop_id,
            "reference": self.reference
        }

    @staticmethod
    def from_dict(id, source):
        return RouteStop(
            id,
            source["name"],
            source["route_id"],
            source["stop_id"],
            source["reference"]
        )
        