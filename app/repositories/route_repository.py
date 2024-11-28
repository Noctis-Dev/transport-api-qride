from app.models.route_model import Route

class RouteRepository:
    def __init__(self, db):
        self.db = db

    def save_route(self, route: Route):
        route_ref = self.db.collection('routes').document()  # Sin especificar un ID
        route_ref.set(route.to_dict())
        return route_ref.id