from fastapi import FastAPI
from app.routers import user  # Import your router here

app = FastAPI()

# Include routers
app.include_router(user.router)
