from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    """
    Application settings, loaded from environment variables.
    """
    GEMINI_API_KEY: str
    PINECONE_API_KEY: str
    PINECONE_ENV: str = "gcp-starter"  # Default to free tier environment
    
    # Paths
    THERAPY_GUIDES_DIR: str = "Therapy_Guides"

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()