import asyncio
import random
import json
from datetime import datetime, timedelta
import httpx
import logging
from typing import List

logger = logging.getLogger(__name__)

EVENT_TYPES = [
    "user_login",
    "user_logout",
    "payment_processed",
    "order_created",
    "item_shipped",
    "error_occurred",
    "data_synced"
]

SOURCE_APPS = [
    "auth_service_001",
    "payment_service_002",
    "order_service_003",
    "shipping_service_004",
    "sync_service_005"
]

async def generate_random_event() -> dict:
    event_type = random.choice(EVENT_TYPES)
    source_app = random.choice(SOURCE_APPS)
    
    data_payload = {
        "timestamp": datetime.utcnow().isoformat(),
        "user_id": f"user_{random.randint(1, 1000)}",
        "transaction_id": f"txn_{random.randint(10000, 99999)}",
        "status": random.choice(["success", "pending", "failed"])
    }
    
    return {
        "event_type": event_type,
        "source_app_id": source_app,
        "data_payload": data_payload
    }

async def send_events(num_events: int, base_url: str = "http://localhost:8000/api/v1"):
    async with httpx.AsyncClient() as client:
        for i in range(num_events):
            try:
                event = await generate_random_event()
                response = await client.post(
                    f"{base_url}/events/",
                    json=event
                )
                response.raise_for_status()
                logger.info(f"Event {i+1}/{num_events} sent successfully")
                await asyncio.sleep(0.1)  # Rate limiting
            except Exception as e:
                logger.error(f"Failed to send event {i+1}: {str(e)}")