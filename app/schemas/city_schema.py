from pydantic import BaseModel

class CityCreate(BaseModel):
    name: str

class CityResponse(BaseModel):
    id: str