from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql://postgres:postgres@localhost:5433/wealthy_dashboard"
    DEBUG: bool = True
    
    class Config:
        env_file = ".env"


settings = Settings()
