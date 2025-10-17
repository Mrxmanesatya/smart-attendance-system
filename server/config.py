"""
Configuration module for Smart Attendance System
Loads environment variables and provides application settings
"""
import os
from typing import List
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""
    
    # MongoDB Configuration
    mongodb_url: str = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
    database_name: str = os.getenv("DATABASE_NAME", "smart_attendance")
    
    # JWT Configuration
    secret_key: str = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
    algorithm: str = os.getenv("ALGORITHM", "HS256")
    access_token_expire_minutes: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "1440"))
    
    # QR Code Configuration
    qr_code_expiry_minutes: int = int(os.getenv("QR_CODE_EXPIRY_MINUTES", "15"))
    
    # CORS Configuration
    cors_origins: List[str] = os.getenv(
        "CORS_ORIGINS", 
        "http://localhost:5173,http://localhost:3000"
    ).split(",")
    
    # Server Configuration
    host: str = os.getenv("HOST", "0.0.0.0")
    port: int = int(os.getenv("PORT", "8000"))
    
    class Config:
        env_file = ".env"


settings = Settings()
