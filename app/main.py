from fastapi import FastAPI
from app.routers import task, user, auth
from app.config import engine, Base

app = FastAPI()

app.include_router(task.router)
app.include_router(user.router)
app.include_router(auth.router)

# To create table during db initialization
Base.metadata.create_all(bind=engine)