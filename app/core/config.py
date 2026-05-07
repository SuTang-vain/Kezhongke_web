from pydantic_settings import BaseSettings, SettingsConfigDict
import os

class Settings(BaseSettings):
    PROJECT_NAME: str = "Kezhongke API"
    DATABASE_URL: str = "postgresql+asyncpg://kezhongke:password123@localhost:5432/kezhongke_db"
    REDIS_URL: str = "redis://localhost:6379/0"
    
    SECRET_KEY: str = "super-secret-key-change-me-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Alibaba Cloud Credentials
    ALIBABA_CLOUD_ACCESS_KEY_ID: str = ""
    ALIBABA_CLOUD_ACCESS_KEY_SECRET: str = ""
    
    # Mail settings
    EMAILS_FROM_EMAIL: str = "noreply@kezhongke.cn"
    SMTP_TLS: bool = True
    SMTP_PORT: int = 587
    SMTP_HOST: str = ""
    SMTP_USER: str = ""
    SMTP_PASSWORD: str = ""

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
