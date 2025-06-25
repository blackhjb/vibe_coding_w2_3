import os
from pydantic import BaseModel, ConfigDict
from typing import Optional

class Settings(BaseModel):
    """Application settings"""
    
    model_config = ConfigDict(
        env_file=".env",
        case_sensitive=False,
        extra='ignore'  # Ignore extra environment variables
    )
    
    # Google Gemini Configuration
    google_api_key: str = ""
    
    # LangSmith Configuration
    langsmith_api_key: str = ""
    langsmith_project: str = "vibe-coding-chatbot"
    
    # FastAPI Configuration
    fastapi_host: str = "127.0.0.1"
    fastapi_port: int = 8000
    
    # Environment
    environment: str = "development"
    
    def __init__(self, **kwargs):
        # Load environment variables with defaults
        env_data = {
            'google_api_key': os.getenv("GOOGLE_API_KEY", ""),
            'langsmith_api_key': os.getenv("LANGSMITH_API_KEY", ""),
            'langsmith_project': os.getenv("LANGSMITH_PROJECT", "vibe-coding-chatbot"),
            'fastapi_host': os.getenv("FASTAPI_HOST", "127.0.0.1"),
            'fastapi_port': int(os.getenv("FASTAPI_PORT", "8000")),
            'environment': os.getenv("ENVIRONMENT", "development"),
        }
        super().__init__(**env_data, **kwargs)

# Global settings instance
settings = Settings() 