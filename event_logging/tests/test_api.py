# tests/test_api.py
import pytest
from httpx import AsyncClient
from datetime import datetime, timedelta

from app.main import app

@pytest.mark.asyncio
async def test_create_event():
    async with AsyncClient(app=app, base_url="http://test") as client:
        event_data = {
            "event_type": "test_event",
            "source_app_id": "test_app",
            "timestamp": datetime.utcnow().isoformat(),
            "payload": {
                "test_key": "test_value"
            }
        }
        
        response = await client.post("/api/events", json=event_data)
        assert response.status_code == 200
        assert "event_id" in response.json()

@pytest.mark.asyncio
async def test_query_events():
    async with AsyncClient(app=app, base_url="http://test") as client:
        # First create some test events
        for _ in range(3):
            event_data = {
                "event_type": "test_event",
                "source_app_id": "test_app",
                "timestamp": datetime.utcnow().isoformat(),
                "payload": {"test_key": "test_value"}
            }
            await client.post("/api/events", json=event_data)
        
        # Query events
        response = await client.get("/api/events")
        assert response.status_code == 200
        events = response.json()
        assert len(events) >= 3
        
        # Test filtering
        start_time = (datetime.utcnow() - timedelta(hours=1)).isoformat()
        response = await client.get(f"/api/events?start_time={start_time}&event_type=test_event")
        assert response.status_code == 200
        
@pytest.mark.asyncio
async def test_verify_chain():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/api/events/verify")
        assert response.status_code == 200
        result = response.json()
        assert "valid" in result
        assert "inconsistencies" in result