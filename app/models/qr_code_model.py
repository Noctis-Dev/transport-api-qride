class QrCode:
    def __init__(self, id, data, route_stop_id):
        self.id = id
        self.data = data
        self.route_stop_id = route_stop_id
    
    def to_dict(self):
        return {
            'data': self.data,
            'route_stop_id': self.route_stop_id
        }
    
    @staticmethod
    def from_dict(id, data):
        return QrCode(
            id, 
            data['data'], 
            data['route_stop_id'],
        )
    
    