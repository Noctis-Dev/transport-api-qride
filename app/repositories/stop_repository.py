from app.models.stop_model import Stop

class StopRepository:
    def __init__(self, db):
        self.db = db

    def save_stop(self, stop: Stop):
        stop_ref = self.db.collection('stops').document()  # Sin especificar un ID
        stop_ref.set(stop.to_dict())
        return stop_ref.id 