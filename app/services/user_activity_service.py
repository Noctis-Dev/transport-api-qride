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
