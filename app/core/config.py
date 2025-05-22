from pathlib import Path
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    FRONTEND_URL:str

    DATABASE_URL: str
    SUPERUSER_DATABASE_URL: str
    DATABASE_NAME: str
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    ENVIRONMENT: str = "development"

    MAIL_USERNAME: str
    MAIL_PASSWORD: str
    MAIL_SERVER: str
    MAIL_FROM: str
    MAIL_FROM_NAME: str

    CLOUDINARY_CLOUD_NAME: str
    CLOUDINARY_API_KEY: str
    CLOUDINARY_API_SECRET: str

    class Config:
        env_file = Path(__file__).resolve().parents[2] / ".env"
        env_file_encoding = "utf-8"

settings = Settings()