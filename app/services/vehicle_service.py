from app.repositories.vehicle_repository import VehicleRepository
from app.schemas.vehicle_schema import VehicleCreate
from app.models.vehicle_model import Vehicle


class VehicleService:

    def __init__(self, db: any):
        self.vehicle_repository = VehicleRepository(db)

    def create_vehicle(self, vehicle: VehicleCreate):
        vehicle = Vehicle.from_dict(vehicle)
        self.vehicle_repository.create_vehicle(vehicle)
        return vehicle