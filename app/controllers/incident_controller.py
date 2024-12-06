from fastapi import APIRouter, Depends, HTTPException
from app.db import get_firestore_db
from app.services.incident_service import IncidentService
from app.schemas.incident_schema import IncidentRequest
import logging

router = APIRouter()

@router.post("/incidents")
async def create_incident(incident_request: IncidentRequest, db=Depends(get_firestore_db)):
    logging.info(f"Creating incident {incident_request}")
    service = IncidentService(db)
    response = service.save_incident(incident_request)
    return response

@router.get("/incidents/{incident_id}")
async def get_incident(incident_id: str, db=Depends(get_firestore_db)):
    logging.info(f"Retrieving incident {incident_id}")
    service = IncidentService(db)
    response = service.get_incident(incident_id)
    return response

@router.get("/incidents")
async def list_incidents(db=Depends(get_firestore_db)):
    logging.info("Listing incidents")
    service = IncidentService(db)
    response = service.list_incidents()
    return response