class Vehicle:
    def __init__(self, id, economic_number, route_id, current_location, status):
        self.id = id
        self.economic_number = economic_number
        self.route_id = route_id
        self.current_location = current_location
        self.status = status

    def to_dict(self):
        return {
            "economic_number": self.economic_number,
            "route_id": self.route_id,
            "current_location": self.current_location,
            "status": self.status
        }

    @staticmethod
    def from_dict(id, source):
        return Vehicle(
            id,
            source["economic_number"],
            source["route_id"],
            source["current_location"],
            source["status"],
        )