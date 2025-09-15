from fastapi import FastAPI
from .database import Base, engine
from .models import users


app = FastAPI(title="Event Manager API")

Base.metadata.create_all(engine)
