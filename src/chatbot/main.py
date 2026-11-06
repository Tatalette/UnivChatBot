from contextlib import asynccontextmanager

from fastapi import FastAPI

from chatbot.api import ask, health, reject, validate
from chatbot.db.session import engine
from chatbot.models.db import Base


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Crée les tables si elles n'existent pas (idempotent)
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(title="Chatbot GLPI", version="0.1.0", lifespan=lifespan)

app.include_router(health.router, tags=["health"])
app.include_router(ask.router, tags=["chatbot"])
app.include_router(validate.router, tags=["chatbot"])
app.include_router(reject.router, tags=["chatbot"])