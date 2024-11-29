from pydantic import BaseModel

class Stop(BaseModel):
    latitude: float
    longitude: float