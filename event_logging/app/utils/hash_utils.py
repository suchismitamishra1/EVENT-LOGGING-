import hashlib
import json
from datetime import datetime

def calculate_hash(event_data: dict) -> str:
    """Calculate SHA-256 hash of event data including previous hash."""
    # Create a copy of the event data
    event_copy = event_data.copy()
    
    # Remove hash if it exists as we don't want to include it in the new hash calculation
    event_copy.pop('hash', None)
    
    # Convert datetime objects to ISO format strings for consistent hashing
    for key, value in event_copy.items():
        if isinstance(value, datetime):
            event_copy[key] = value.isoformat()
    
    # Sort keys for consistent hashing
    serialized = json.dumps(event_copy, sort_keys=True)
    
    # Calculate and return SHA-256 hash
    return hashlib.sha256(serialized.encode()).hexdigest()

def verify_hash(event_data: dict) -> bool:
    """Verify if the stored hash matches the calculated hash."""
    stored_hash = event_data.get('hash')
    if not stored_hash:
        return False
        
    calculated = calculate_hash(event_data)
    return stored_hash == calculated