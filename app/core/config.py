# app/core/config.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    data_file: str = "patients.json"

settings = Settings()
