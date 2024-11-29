from app.models.stop_model import Stop

class StopRepository:
    def __init__(self, db):
        self.db = db

    def save_stop(self, stop: Stop):
        stop_ref = self.db.collection('stops').document()  # Sin especificar un ID
        stop_ref.set(stop.to_dict())
        return stop_ref.id 
    
    def get_stop_by_id(self, stop_id: str) -> Stop:
        stop_ref = self.db.collection('stops').document(stop_id)
        stop_doc = stop_ref.get()
        if stop_doc.exists:
            return Stop.from_dict(stop_ref.id, stop_doc.to_dict())
        else:
            return None