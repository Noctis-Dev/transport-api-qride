from app.schemas.user_activity_schema import RequestUserActivity

class UserActivity:
    def __init__(self, user_id, latitude, longitude, is_active):
        self.user_id = user_id
        self.latitude = latitude
        self.longitude = longitude
        self.is_active = is_active

    def to_dict(self):
        return {
            'latitude': self.latitude,
            'longitude': self.longitude,
            'is_active': self.is_active,
        }
    
    @staticmethod
    def from_dict(user_id, source):
        return UserActivity(
            user_id,
            source["latitude"],
            source["longitude"],
            source["is_active"]
        )
        
    @staticmethod
    def from_request(user_activity_create: RequestUserActivity):
        return UserActivity(
            user_id=user_activity_create.user_id,
            latitude=user_activity_create.latitude,
            longitude=user_activity_create.longitude,
            is_active=user_activity_create.is_active
        )