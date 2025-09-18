"""
FastAPI application entry point.

Initializes the app, creates database tables at startup using the lifespan
context, and registers the patient API router.
"""
from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.core.database import Base, engine
from app.routers.patient_router import router as patient_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield  

app = FastAPI(lifespan=lifespan)
app.include_router(patient_router)
