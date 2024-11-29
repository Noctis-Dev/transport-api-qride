from app.repositories.route_stop_repository import RouteStopRepository
from app.models.route_stop_model import RouteStop
from app.schemas.route_stop_schema import RouteStopRequest, RouteStopResponse
from app.services.stop_service import StopService
from app.schemas.route_stop_schema import NearbyStopsRequest as NearbyRoutStopsRquest


class RouteStopService:
    def __init__(self, db: any):
        self.route_stop_repository = RouteStopRepository(db)
        self.stop_service = StopService(db)

    def create_route_stop(self, route_stop: RouteStopRequest):
        stop_id = self.stop_service.create_stop(route_stop.stop)
        route_stop = RouteStop.from_request(route_stop, stop_id)
        route_stop_id = self.route_stop_repository.create_route_stop(route_stop)
        return RouteStopResponse(route_stop_id=route_stop_id, name=route_stop.name)

    def get_nearby_route_stops (self, request: NearbyRoutStopsRquest):
        return self.route_stop_repository.get_nearby_route_stops(request.latitude, request.longitude, request.radius)