import uvicorn
import asyncio
import logging
from app.main import app
from scripts.monitor_chain import ChainMonitor

async def start_monitor():
    monitor = ChainMonitor()
    await monitor.monitor_events()

if __name__ == "__main__":
    # Setup logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Start the monitor in the background
    loop = asyncio.get_event_loop()
    loop.create_task(start_monitor())
    
    # Run the FastAPI application
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )