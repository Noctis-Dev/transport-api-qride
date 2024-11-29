from app.models.route_stop_model import RouteStop 
from geopy.distance import geodesic


class RouteStopRepository:
    def __init__(self, db):
        self.db = db

    def create_route_stop(self, route_stop: RouteStop):
        route_stop_ref = self.db.collection('route_stops').document()
        route_stop_ref.set(route_stop.to_dict())
        return route_stop_ref.id
    
    def get_nearby_route_stops(self, latitude: float, longitude: float, radius: float):
        all_stops_ref = self.db.collection('route_stops').stream()
        nearby_stops = []

        user_location = (latitude, longitude)

        for stop_doc in all_stops_ref:
            stop_data = stop_doc.to_dict()
            stop_location = (stop_data['latitude'], stop_data['longitude'])
            
            if stop_location[0] is not None and stop_location[1] is not None:
                distance = geodesic(user_location, stop_location).kilometers
                if distance <= radius:
                    
                    stop = RouteStop.from_dict(stop_doc.id, stop_dict)
                    nearby_stops.append(stop)

        return nearby_stops