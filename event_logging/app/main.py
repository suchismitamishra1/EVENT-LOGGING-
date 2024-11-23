# File: app/main.py
from fastapi import FastAPI
from .routes import event_routes
from .config import settings

app = FastAPI(
    title="Event Logging System",
    description="A scalable, tamper-proof event logging platform",
    version=settings.API_VERSION
)

app.include_router(event_routes.router, prefix=f"/api/{settings.API_VERSION}")
