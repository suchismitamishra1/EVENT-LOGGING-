# File: scripts/monitor_chain.py
import asyncio
import httpx
import logging
from datetime import datetime
from typing import Dict, List

logger = logging.getLogger(__name__)

class ChainMonitor:
    def __init__(self, base_url: str = "http://localhost:8000/api/v1"):
        self.base_url = base_url
        self.last_check = datetime.utcnow()
    
    async def check_chain_integrity(self) -> Dict:
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(f"{self.base_url}/verify-chain/")
                response.raise_for_status()
                return response.json()
            except Exception as e:
                logger.error(f"Chain integrity check failed: {str(e)}")
                return {"chain_valid": False, "error": str(e)}
    
    async def monitor_events(self, interval_seconds: int = 60):
        while True:
            try:
                result = await self.check_chain_integrity()
                if result.get("chain_valid"):
                    logger.info("Chain integrity verified successfully")
                else:
                    logger.error("Chain integrity verification failed!")
                    
                # Get recent events
                async with httpx.AsyncClient() as client:
                    response = await client.get(
                        f"{self.base_url}/events/",
                        params={"limit": 10}
                    )
                    recent_events = response.json()
                    logger.info(f"Recent events count: {len(recent_events)}")
                    
            except Exception as e:
                logger.error(f"Monitoring error: {str(e)}")
            
            await asyncio.sleep(interval_seconds)
