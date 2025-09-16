from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str # default local sqlite
    # agar .env use kar rahe ho:
    class Config:
        env_file = ".env"

settings = Settings()
