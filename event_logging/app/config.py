from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    MONGODB_URL: str = Field(default="mongodb://localhost:27017")
    DATABASE_NAME: str = Field(default="event_logging")
    API_VERSION: str = Field(default="v1")
    PAGE_SIZE: int = Field(default=100)

    class Config:
        env_file = ".env"
        case_sensitive = False

settings = Settings()