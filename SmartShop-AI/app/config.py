from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    GEMINI_API_KEY: str 
    DATABASE_URL: str = "sqlite:///./ecommerce.db"
    MODEL_NAME: str = "gemini-1.5-flash"
    
    class Config:
        env_file = ".env"

@lru_cache()
def get_settings():
    return Settings()