from app.repositories.route_stop_repository import RouteStopRepository
from app.models.route_stop_model import RouteStop
from app.schemas.route_stop_schema import RouteStopRequest, RouteStopResponse
from app.services.stop_service import StopService
from app.schemas.route_stop_schema import NearbyStopsRequest
from app.schemas.stop_schema import Stop
from geopy.distance import geodesic
from geopy.point import Point
import random


class RouteStopService:
    def __init__(self, db: any):
        self.route_stop_repository = RouteStopRepository(db)
        self.stop_service = StopService(db)

    def create_route_stop(self, route_stop: RouteStopRequest):
        stop_id = self.stop_service.create_stop(route_stop.stop)
        route_stop = RouteStop.from_request(route_stop, stop_id)
        route_stop_id = self.route_stop_repository.create_route_stop(route_stop)
        return RouteStopResponse(route_stop_id=route_stop_id, name=route_stop.name)

    def get_nearby_route_stops(self, request: NearbyStopsRequest):
        all_stops = self.route_stop_repository.get_all_route_stops()
        nearby_stops = []

        for stop in all_stops:
            stop_id = stop.id
            stop = self.stop_service.get_stop_by_id(stop_id)
            stop_location = (stop.latitude, stop.longitude)
            request_location = (request.latitude, request.longitude)
            distance = geodesic(stop_location, request_location).kilometers

            if distance <= request.radius:
                nearby_stops.append(stop)

        return nearby_stops
    
    @staticmethod
    def generate_random_coordinates(reference_point, radius_km):
        # Generate a random distance and angle
        distance = random.uniform(0, radius_km)
        angle = random.uniform(0, 360)

        # Calculate the new point
        origin = Point(reference_point)
        destination = geodesic(kilometers=distance).destination(origin, angle)
        return destination.latitude, destination.longitude

    def generate_random_route_stops(self, reference_point, radius_km, num_stops):
        route_stops = []
        for _ in range(num_stops):
            lat, lon = self.generate_random_coordinates(reference_point, radius_km)
            stop = Stop(
                latitude=lat,
                longitude=lon,
            )
            stop_id = self.stop_service.create_stop(stop)
            route_stop = RouteStop(
                id=None,
                name=f"Stop {_}",
                reference="",
                route=[f"{_}", f"{_+1}"],
                stop_id=stop_id,
            )
            route_stops.append(route_stop)
        for route in route_stops:
            self.route_stop_repository.create_route_stop(route)
        pass