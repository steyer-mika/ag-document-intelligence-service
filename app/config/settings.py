"""
Configuration
"""
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # API Configuration
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()