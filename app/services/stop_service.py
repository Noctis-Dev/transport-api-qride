from app.models.stop_model import Stop as StopModel
from app.repositories.stop_repository import StopRepository
from app.schemas.stop_schema import Stop
from typing import List

class StopService:
    def __init__(self, db):
        self.stop_repository = StopRepository(db)

    def create_stop(self, stop: Stop):
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
    
    def get_stop_by_id(self, stop_id: str) -> StopModel:
        stop = self.stop_repository.get_stop_by_id(stop_id)
        if stop:
            return stop
        else:
            return None
