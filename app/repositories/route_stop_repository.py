from app.models.route_stop_model import RouteStop 

class RouteStopRepository:
    def __init__(self, db):
        self.db = db

    def create_route_stop(self, route_stop: RouteStop):
        route_stop_ref = self.db.collection('route_stops').document()
        route_stop_ref.set(route_stop.to_dict())
        return route_stop_ref.id
    
    def get_all_route_stops(self):
        all_stops_ref = self.db.collection('route_stops').stream()
        all_stops = []

        for stop_doc in all_stops_ref:
            stop_data = stop_doc.to_dict()
            stop = RouteStop.from_dict(stop_doc.id, stop_data)
            all_stops.append(stop)

        return all_stops