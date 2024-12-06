from app.models.vehicle_model import Vehicle


class VehicleRepository:

    def __init__(self, db: any):
        self.db = db
        
    def create_vehicle(self, vehicle: Vehicle):
        vehicle_ref = self.db.collection('users').document()
        vehicle_ref.set(vehicle.to_dict())