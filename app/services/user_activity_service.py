import random
from geopy.distance import geodesic
from geopy.point import Point
from app.models.user_activity_model import UserActivity
from app.repositories.user_activity_repository import UserActivityRepository
from app.schemas.user_activity_schema import RequestUserActivity, ResponseUserActivity

class UserActivityService:
    def __init__(self, db: any):
        self.user_activity_repository = UserActivityRepository(db)

    def log_user_activity(self, user_activity: RequestUserActivity):
        user_activity = UserActivity.from_request(user_activity)
        user_activity_id = self.user_activity_repository.save_user_activity(user_activity)
        return ResponseUserActivity(message="activity logged", activity_id=user_activity_id)

    
    @staticmethod
    def generate_random_coordinates(reference_point, radius_km):
        # Generate a random distance and angle
        distance = random.uniform(0, radius_km)
        angle = random.uniform(0, 360)

        # Calculate the new point
        origin = Point(reference_point)
        destination = geodesic(kilometers=distance).destination(origin, angle)
        return destination.latitude, destination.longitude

    def generate_random_user_activities(self, reference_point, radius_km, num_activities):
        for _ in range(num_activities):
            lat, lon = self.generate_random_coordinates(reference_point, radius_km)
            user_activity = RequestUserActivity(
                user_id=f"user_{random.randint(1, 1000)}",
                latitude=lat,
                longitude=lon,
                is_active=True
            )
            response = self.log_user_activity(user_activity)
            print(f"User activity logged with id: {response.activity_id}")