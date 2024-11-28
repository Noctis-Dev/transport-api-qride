from app.models.route_stop_model import RouteStop  # Asegúrate de importar el modelo

class RouteStopRepository:
    def __init__(self, db):
        self.db = db

    def create_route_stop(self, route_id: str, stop: RouteStop):
        route_stops_collection = self.db.collection('routes').document(route_id).collection('stops')
        new_stop_ref = route_stops_collection.document()  # No necesitas generar el ID manualmente
        new_stop_ref.set(stop.to_dict())
        return new_stop_ref.id

