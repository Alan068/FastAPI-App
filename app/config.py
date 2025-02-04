from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.settings import settings  # Importing Settings class for db URL

import os
from dotenv import load_dotenv

load_dotenv()  # loads environment variables from .env file


DATABASE_URL = settings.DATABASE_URL # Tells sqlite where to find database

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})   # Connects fastapi to the database, allows same conn to be used across diff threads.

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)   # This session is used to interact with db, with autocommit=false, changes not automlly saved to db. We've to manually commit.

Base = declarative_base()   # Foundation for all db models. Helps sqlalechemy manage the models and map em to db tables.

# To get db session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()