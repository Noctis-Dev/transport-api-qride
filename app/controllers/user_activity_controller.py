from fastapi import APIRouter, Depends, HTTPException
from app.db import get_firestore_db
from app.services.user_activity_service import UserActivityService
from app.schemas.user_activity_schema import RequestUserActivity, ResponseUserActivity
from app.schemas.base_response import BaseResponse
import logging

router = APIRouter()

@router.post("/log_activity/{user_uuid}", response_model=BaseResponse)
async def log_activity(user_uuid: str, request_user_activity: RequestUserActivity, db=Depends(get_firestore_db)):
    request_user_activity.user_id = user_uuid
    try:
        logging.info(f"Logging activity for user: {user_uuid}")
        user_activity_service = UserActivityService(db)
        user_activity = user_activity_service.log_user_activity(request_user_activity)
        logging.info(f"Activity logged successfully for user: {user_uuid}")
        return BaseResponse(data=user_activity, message="activity logged", success=True)
    except Exception as e:
        logging.error(f"Error logging activity for user: {user_uuid} - {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

