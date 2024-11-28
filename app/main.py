from fastapi import FastAPI
from app.controllers.vehicle_controller import router as vehicle_router
from app.controllers.city_controller import router as city_router
from app.controllers.chat_controller import router as chat_router
from app.controllers.user_activity_controller import router as user_activity_router
from app.controllers.route_controller import router as route_router
import app.listener.heatmap_listener

app = FastAPI()

app.include_router(vehicle_router , prefix="/api/v1")
app.include_router(city_router , prefix="/api/v1")
app.include_router(chat_router , prefix="/api/v1")
app.include_router(user_activity_router , prefix="/api/v1")
app.include_router(route_router , prefix="/api/v1")

@app.get("/")
def read_root():
    return {"message": "Welcome to Qride API"}

