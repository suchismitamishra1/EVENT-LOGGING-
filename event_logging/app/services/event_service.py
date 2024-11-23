# File: app/services/event_service.py
from typing import List, Optional
from datetime import datetime
from pymongo import MongoClient, ASCENDING, DESCENDING
from ..config import settings
from ..models.event import Event
# from .hash_service import HashService


class EventService:
    def __init__(self):
        self.client = MongoClient(settings.MONGODB_URL)
        self.db = self.client[settings.DATABASE_NAME]
        self.events = self.db.events
        self._setup_indexes()

    def _setup_indexes(self):
        # Create indexes for efficient querying
        self.events.create_index([("timestamp", ASCENDING)])
        self.events.create_index([("event_type", ASCENDING)])
        self.events.create_index([("source_app_id", ASCENDING)])

    async def create_event(self, event: Event) -> dict:
        # Get the last event to link the chain
        last_event = self.events.find_one(sort=[("timestamp", DESCENDING)])
        
        # Convert Event to dict for manipulation
        event_dict = event.dict()
        
        # Set the previous hash if there's a last event
        if last_event:
            event_dict['previous_hash'] = last_event['current_hash']
        
        # Calculate current hash
        # event_dict['current_hash'] = HashService.calculate_hash(event_dict)
        
        # Insert the event
        result = self.events.insert_one(event_dict)
        event_dict['_id'] = str(result.inserted_id)
        
        return event_dict

    async def get_events(
        self,
        skip: int = 0,
        limit: int = settings.PAGE_SIZE,
        event_type: Optional[str] = None,
        source_app_id: Optional[str] = None,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None
    ) -> List[dict]:
        # Build query filter
        query = {}
        if event_type:
            query['event_type'] = event_type
        if source_app_id:
            query['source_app_id'] = source_app_id
        if start_time or end_time:
            query['timestamp'] = {}
            if start_time:
                query['timestamp']['$gte'] = start_time
            if end_time:
                query['timestamp']['$lte'] = end_time

        # Execute query with pagination
        events = list(self.events.find(
            query,
            skip=skip,
            limit=limit
        ).sort("timestamp", DESCENDING))

        # Convert ObjectId to string for JSON serialization
        for event in events:
            event['_id'] = str(event['_id'])

        return events

    async def verify_chain_integrity(self) -> bool:
        events = list(self.events.find().sort("timestamp", ASCENDING))
        
        for i in range(len(events)):
            current_event = events[i]
            
            # Verify current hash
            # calculated_hash = HashService.calculate_hash(current_event)
            # if calculated_hash != current_event['current_hash']:
                # return False
            
            # Verify chain link (except for first event)
            if i > 0:
                previous_event = events[i-1]
                if current_event['previous_hash'] != previous_event['current_hash']:
                    return False
        
        return True
