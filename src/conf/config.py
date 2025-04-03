import os

from dotenv import load_dotenv

load_dotenv()


class Config:
    DB_URL = os.environ.get('DB_URL')
    JWT_SECRET = os.environ.get('JWT_SECRET')
    JWT_ALGORITHM = os.environ.get('JWT_ALGORITHM', "HS256")
    JWT_EXPIRATION_SECONDS = int(os.environ.get('JWT_EXPIRATION_SECONDS', 3600))


config = Config
