from app.models.route_model import Route

class RouteRepository:
    def __init__(self, db):
        self.db = db

    def save_route(self, route: Route):
        route_ref = self.db.collection('routes').document()  # Sin especificar un ID
        route_ref.set(route.to_dict())
        return route_ref.id
    
    def get_all_routes(self):
        all_routes_ref = self.db.collection('routes').stream()
        all_routes = []

        for route_doc in all_routes_ref:
            route_data = route_doc.to_dict()
            route = Route.from_dict(route_doc.id, route_data)
            all_routes.append(route.to_dict())
                              
        return all_routes