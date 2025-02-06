from pydantic_settings import BaseSettings
import os
from dotenv import load_dotenv
# from app.routers.auth import SECRET_KEY

class Settings(BaseSettings):
    DATABASE_URL: str = os.getenv("DATABASE_URL")
    SECRET_KEY: str = os.getenv("SECRET_KEY")

    class Config:
        env_file = ".env"  # The .env file to load from


settings = Settings()  # Initializing settings