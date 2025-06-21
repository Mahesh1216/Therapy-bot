from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """
    Application settings, loaded from environment variables.
    """
    GEMINI_API_KEY: str
    PINECONE_API_KEY: str

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()