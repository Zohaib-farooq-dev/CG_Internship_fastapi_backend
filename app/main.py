"""
FastAPI application entry point.

Initializes the app, creates database tables at startup using the lifespan
context, and registers the patient, doctor, and auth routers.
"""
from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.core.database import Base, engine
from app.routers.patient_router import router as patient_router
from app.routers.doctor_router import router as doctor_router
from app.routers.auth import router as authrouter 
# from app.models.doctor_models import Doctor
# from app.models.patient_models import Patient


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield  

app = FastAPI(lifespan=lifespan)
app.include_router(patient_router)
app.include_router(doctor_router)
app.include_router(authrouter)
