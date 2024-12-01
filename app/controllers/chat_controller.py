from fastapi import APIRouter, Depends, HTTPException
from app.db import get_realtime_db
from app.services.chat_service import ChatService
from app.schemas.chat_schema import RequestMessage, ResponseMessage
from app.schemas.base_response import BaseResponse
import logging

router = APIRouter()

@router.post("/chats/{route_name}/messages/", response_model=BaseResponse)
async def post_message(route_name: str, message_create: RequestMessage, db=Depends(get_realtime_db)):
    try:
        chat_service = ChatService(db)
        message_id = chat_service.send_message(route_name, message_create.user, message_create.message)
        
        # Detectar palabras clave y crear una incidencia si es necesario
        if chat_service.analyze_message(message_create.message):
            chat_service.create_incident(message_create.user, message_create.message)
        
        response = ResponseMessage(
            message='Message sent successfully',
            message_id=message_id
        )
        
        return BaseResponse(data=response, message='Message sent', success=True, error="" ) 
    except Exception as e:
        logging.error(f"Error in post_message: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))