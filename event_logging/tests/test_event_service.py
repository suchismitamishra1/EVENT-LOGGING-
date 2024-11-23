import pytest
from datetime import datetime
from app.services.event_service import EventService
from app.models.event import Event

@pytest.fixture
def event_service():
    return EventService()

@pytest.mark.asyncio
async def test_create_event(event_service):
    event = Event(
        event_type="test_event",
        source_app_id="test_app",
        data_payload={"test": "data"}
    )
    
    created_event = await event_service.create_event(event)
    assert created_event['event_type'] == "test_event"
    assert created_event['current_hash'] is not None

@pytest.mark.asyncio
async def test_chain_integrity(event_service):
    # Create multiple events
    for i in range(3):
        event = Event(
            event_type=f"test_event_{i}",
            source_app_id="test_app",
            data_payload={"test": f"data_{i}"}
        )
        await event_service.create_event(event)
    
    # Verify chain integrity
    is_valid = await event_service.verify_chain_integrity()
    assert is_valid is True