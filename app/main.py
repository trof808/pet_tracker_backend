from .schemas import user
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine
from app.models import task, user
from app.api import users, tasks

user.Base.metadata.create_all(bind=engine)
task.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users.router)
app.include_router(tasks.router, prefix="/api/v1")


@app.get("/")
def read_root():
    return {"message": "Welcome to the Calendar API"}
