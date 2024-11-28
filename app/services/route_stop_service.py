from app.repositories.route_stop_repository import RouteStopRepository
from app.models.route_stop_model import RouteStop
from app.schemas.route_stop_schema import RouteStopRequest, RouteStopResponse


class RouteStopService:
    def __init__(self, db: any):
        self.route_stop_repository = RouteStopRepository(db)

    def create_route_stop(self, route_id: str, stop: RouteStopRequest):
         # Convertir a modelo de dominio:
        stop_dict = stop.dict()
        stop_model = RouteStop(id=None, name=stop_dict["name"],  stop_id=stop_dict.get("stop_id"), reference=stop_dict.get("reference")) # Corregir la instanciación

        new_stop_id = self.route_stop_repository.create_route_stop(route_id, stop_model)

        return RouteStopResponse(message="Route stop created successfully", stop_id=new_stop_id, route_id=route_id)  # Devolver el ID de la parada y la ruta


