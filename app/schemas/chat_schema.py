from pydantic import BaseModel

class RequestMessage(BaseModel):
    message: str
    user: str

class ResponseMessage(BaseModel):
    message: str
    message_id: str
