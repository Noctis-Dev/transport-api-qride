from app.models.route_model import Route
from app.repositories.route_repository import RouteRepository
from app.services.stop_service import StopService
from app.schemas.route_schema import RouteRequest, RouteResponse

class RouteService:
    def __init__(self, db):
        self.route_repository = RouteRepository(db)
        self.stop_service = StopService(db)
        
    def create_route(self, route: RouteRequest):
        stops_ids = self.stop_service.create_stops(route.stops)
        route = Route.from_request(route, stops_ids)
        route_id = self.route_repository.save_route(route)
        return RouteResponse(id=route_id, name=route.name, city_id=route.city_id, stops=route.stops)
    
    def get_all_routes(self):
        return self.route_repository.get_all_routes()