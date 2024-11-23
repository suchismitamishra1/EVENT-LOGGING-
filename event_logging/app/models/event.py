from datetime import datetime
from typing import Dict, Optional
from pydantic import BaseModel, Field

class Event(BaseModel):
    event_type: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    source_app_id: str
    data_payload: Dict
    previous_hash: Optional[str] = None
    current_hash: Optional[str] = None

    model_config = {
        "json_schema_extra": {
            "example": {
                "event_type": "user_login",
                "source_app_id": "auth_service_001",
                "data_payload": {
                    "user_id": "123",
                    "login_method": "oauth"
                }
            }
        }
    }