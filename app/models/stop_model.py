class Stop:
    def __init__(self, id, latitude, longitude):
        self.id = id
        self.latitude = latitude
        self.longitude = longitude

    def to_dict(self):
        return {
            "latitude": self.latitude,
            "longitude": self.longitude
        }

    @staticmethod
    def from_dict(id, source):
        return Stop(
            id,
            source["latitude"],
            source["longitude"]
        )