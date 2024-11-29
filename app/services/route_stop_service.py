from app.repositories.route_stop_repository import RouteStopRepository
from app.models.route_stop_model import RouteStop
from app.schemas.route_stop_schema import RouteStopRequest, RouteStopResponse
from app.services.stop_service import StopService
from app.schemas.route_stop_schema import NearbyStopsRequest, NearbyStops, NearbyStopsResponse
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

        request_location = (float(request.latitude), float(request.longitude))
        print(f"Request location: {request_location}")

        for route_stop in all_stops:
            stop_id = route_stop.stop_id
            stop = self.stop_service.get_stop_by_id(stop_id)
            stop_location = (float(stop.latitude), float(stop.longitude))
            print(f"Stop location: {stop_location}")

            # Verifica que las coordenadas estén dentro del rango permitido
            if not (-90 <= stop_location[0] <= 90 and -180 <= stop_location[1] <= 180):
                print(f"Invalid stop location: {stop_location}")
                continue

            distance = geodesic(stop_location, request_location).kilometers

            if distance <= request.radius:
                nearby_stops.append(NearbyStops(route_stop_id=route_stop.id, name=route_stop.name, latitude=stop.latitude, longitude=stop.longitude))

        return NearbyStopsResponse(stops=nearby_stops)
    
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
                routes=[f"{_}", f"{_+1}"],
                stop_id=stop_id,
            )
            route_stops.append(route_stop)
        for route in route_stops:
            route_stop = self.route_stop_repository.create_route_stop(route)
            print(f"Route stop created with id: {route_stop}")
        pass