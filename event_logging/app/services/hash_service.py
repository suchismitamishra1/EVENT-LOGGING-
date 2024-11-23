# File: tests/test_hash_service.py
import pytest
from app.services.hash_service import HashService
from datetime import datetime

def test_hash_calculation():
    # Test data
    event_data = {
        "event_type": "test_event",
        "timestamp": datetime.utcnow(),
        "source_app_id": "test_app",
        "data_payload": {"test": "data"}
    }
    
    # Calculate hash
    hash1 = HashService.calculate_hash(event_data)
    hash2 = HashService.calculate_hash(event_data)
    
    # Verify hash is consistent
    assert hash1 == hash2
    assert len(hash1) == 64  # SHA-256 produces 64 character hex string
    
    # Modify data and verify hash changes
    event_data["data_payload"]["test"] = "modified"
    hash3 = HashService.calculate_hash(event_data)
    assert hash1 != hash3