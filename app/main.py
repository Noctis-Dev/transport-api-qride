from fastapi import FastAPI
from app.db import engine, Base, SessionLocal
from app.controllers.vehicle_controller import router as vehicle_router

app = FastAPI()

app.include_router(vehicle_router , prefix="/api/v1")


@app.get("/")
def read_root():
    return {"message": "Welcome to Qride API"}

