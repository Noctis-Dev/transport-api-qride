from fastapi import FastAPI
import threading
import logging
from app.controllers.vehicle_controller import router as vehicle_router
from app.controllers.city_controller import router as city_router
from app.controllers.chat_controller import router as chat_router
from app.controllers.user_activity_controller import router as user_activity_router
from app.controllers.route_controller import router as route_router
from app.controllers.route_stop_controller import router as route_stop_router
from app.controllers.route_stop_controller import router as nearby_route_stops_router
from app.db import get_firestore_db
from app.services.route_stop_service import RouteStopService
from app.services.user_activity_service import UserActivityService
import app.listener.heatmap_listener


db = get_firestore_db()
route_stop_service = RouteStopService(db)
user_activity_service = UserActivityService(db)


app = FastAPI()

app.include_router(vehicle_router , prefix="/api/v1")
app.include_router(city_router , prefix="/api/v1")
app.include_router(chat_router , prefix="/api/v1")
app.include_router(user_activity_router , prefix="/api/v1")
app.include_router(route_router , prefix="/api/v1")
app.include_router(route_stop_router , prefix="/api/v1")
app.include_router(nearby_route_stops_router , prefix="/api/v1")

def start_generate_random_route_stops():
        reference_point = (16.623413, -93.100081)
        radius_km = 10
        num_stops = 10
        threading.Thread(target=route_stop_service.generate_random_route_stops, args=(reference_point, radius_km, num_stops)).start()

def start_generate_random_user_activities():
    reference_point = (16.623413, -93.100081)
    radius_km = 0.5
    num_activities = 10
    threading.Thread(target=user_activity_service.generate_random_user_activities, args=(reference_point, radius_km, num_activities)).start()
    
@app.on_event("startup")
async def startup_event():
    start_generate_random_route_stops()
    start_generate_random_user_activities()

@app.get("/")
def read_root():
    return {"message": "Welcome to Qride API"}

logging.basicConfig(level=logging.DEBUG)


