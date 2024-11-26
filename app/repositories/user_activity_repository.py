from app.models.user_activity_model import UserActivity

class UserActivityRepository:
    def __init__(self, db):
        self.db = db
    
    def save_user_activity(self, user_activity: UserActivity):
        user_activity_ref = self.db.collection('user_activities').document(user_activity.user_id)
        user_activity_ref.set(user_activity.to_dict())
        return user_activity_ref.id