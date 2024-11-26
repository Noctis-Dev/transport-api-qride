from pydantic import BaseModel

class CityCreate(BaseModel):
    name: str

class ResponseCity(BaseModel):
    id: str