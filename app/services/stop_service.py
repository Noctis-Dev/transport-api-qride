from app.models.stop_model import Stop as StopModel
from app.repositories.stop_repository import StopRepository
from app.schemas.route_schema import Stop
from typing import List

class StopService:
    def __init__(self, db):
        self.stop_repository = StopRepository(db)

    def create_stop(self, stop):
        stop = StopModel.from_request(stop)
        stop_id = self.stop_repository.save_stop(stop)
        return stop_id
    
    def create_stops(self, stops: List[Stop]):
        stops_ids = []
        for stop in stops:
            stop = StopModel.from_request(stop)
            stop_id = self.create_stop(stop)
            stops_ids.append(stop_id)
        return stops_ids
