from pydantic import BaseModel
from typing import Any

class BaseResponse(BaseModel):
    message: str
    success: bool = True
    data: Any = None
    error: Any = None