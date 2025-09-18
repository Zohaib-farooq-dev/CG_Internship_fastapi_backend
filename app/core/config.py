"""
Application configuration using environment variables.

Defines the Settings class to load configuration values (e.g., DATABASE_URL)
from a .env file or system environment for flexible deployment.
"""
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str # default local sqlite
    class Config:
        env_file = ".env"

settings = Settings()
