import os

from dotenv import load_dotenv

# load_dotenv()
#
#
# class Config:
#     DB_URL = os.environ.get('DB_URL')
#     JWT_SECRET = os.environ.get('JWT_SECRET')
#     JWT_ALGORITHM = os.environ.get('JWT_ALGORITHM', "HS256")
#     JWT_EXPIRATION_SECONDS = int(os.environ.get('JWT_EXPIRATION_SECONDS', 3600))
#
#
# config = Config


from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    DB_URL: str
    JWT_SECRET: str
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRATION_SECONDS: int = Field(default=3600)

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=True
    )

settings = Settings()