# File: app/routes/event_routes.py
from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from datetime import datetime
from ..models.event import Event
from ..services.event_service import EventService

router = APIRouter()
event_service = EventService()

@router.post("/events/", response_model=Event)
async def create_event(event: Event):
    try:
        created_event = await event_service.create_event(event)
        return created_event
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/events/", response_model=List[Event])
async def get_events(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    event_type: Optional[str] = None,
    source_app_id: Optional[str] = None,
    start_time: Optional[datetime] = None,
    end_time: Optional[datetime] = None
):
    try:
        events = await event_service.get_events(
            skip=skip,
            limit=limit,
            event_type=event_type,
            source_app_id=source_app_id,
            start_time=start_time,
            end_time=end_time
        )
        return events
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/verify-chain/")
async def verify_chain():
    try:
        is_valid = await event_service.verify_chain_integrity()
        return {"chain_valid": is_valid}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))