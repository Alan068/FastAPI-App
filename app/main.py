from fastapi import FastAPI
from app.routers import task
from app.config import engine, Base

app = FastAPI()

app.include_router(task.router)


# To create table, db initialization
Base.metadata.create_all(bind=engine)