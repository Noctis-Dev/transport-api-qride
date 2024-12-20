import logging
import os
from fastapi import FastAPI
from app.controllers.vehicle_controller import router as vehicle_router
from app.controllers.city_controller import router as city_router
from app.controllers.chat_controller import router as chat_router
from app.controllers.user_activity_controller import router as user_activity_router
from app.controllers.route_controller import router as route_router
from app.controllers.route_stop_controller import router as route_stop_router
from app.controllers.route_stop_controller import router as nearby_route_stops_router
from app.controllers.incident_controller import router as incident_router

log_dir = "var/log"
os.makedirs(log_dir, exist_ok=True)

logging.basicConfig(
    filename=os.path.join(log_dir, 'myapp.log'), 
    level=logging.INFO,                             
    format='%(asctime)s - %(levelname)s - %(message)s'  
)

app = FastAPI()

app.include_router(vehicle_router , prefix="/api/v1")
app.include_router(city_router , prefix="/api/v1")
app.include_router(chat_router , prefix="/api/v1")
app.include_router(user_activity_router , prefix="/api/v1")
app.include_router(route_router , prefix="/api/v1")
app.include_router(route_stop_router , prefix="/api/v1")
app.include_router(nearby_route_stops_router , prefix="/api/v1")
app.include_router(incident_router , prefix="/api/v1")

@app.get("/")
def read_root():
    return {"message": "Welcome to Qride API"}



