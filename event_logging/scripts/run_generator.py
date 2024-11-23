import asyncio
import logging
from generate_events import send_events

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

async def main():
    # Generate 50 events (you can change this number)
    await send_events(50)

if __name__ == "__main__":
    asyncio.run(main())