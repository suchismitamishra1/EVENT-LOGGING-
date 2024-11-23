# File: app/utils/validators.py
from datetime import datetime
from typing import Dict, Any
from fastapi import HTTPException

def validate_event_data(event_data: Dict[str, Any]) -> None:
    required_fields = ['event_type', 'source_app_id', 'data_payload']
    
    for field in required_fields:
        if field not in event_data:
            raise HTTPException(
                status_code=400,
                detail=f"Missing required field: {field}"
            )
    
    if not isinstance(event_data['data_payload'], dict):
        raise HTTPException(
            status_code=400,
            detail="data_payload must be a JSON object"
        )
    
    if len(event_data['source_app_id']) < 3:
        raise HTTPException(
            status_code=400,
            detail="source_app_id must be at least 3 characters long"
        )
