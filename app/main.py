from fastapi import FastAPI
import threading
from app.controllers.vehicle_controller import router as vehicle_router
from app.controllers.city_controller import router as city_router
from app.controllers.chat_controller import router as chat_router
from app.controllers.user_activity_controller import router as user_activity_router
from app.controllers.route_controller import router as route_router
from app.controllers.route_stop_controller import router as route_stop_router
from app.controllers.route_stop_controller import router as nearby_route_stops_router
from app.db import get_firestore_db
from app.services.route_stop_service import RouteStopService

db = get_firestore_db()
route_stop_service = RouteStopService(db)

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

@app.get("/")
def read_root():
    return {"message": "Welcome to Qride API"}

