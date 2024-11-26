from pydantic import BaseModel

class RequestUserActivity(BaseModel):
    user_id: str
    latitude: float
    longitude: float
    is_active: bool
    
class ResponseUserActivity(BaseModel):
    message: str
    activity_id: str