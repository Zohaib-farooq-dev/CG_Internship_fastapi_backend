from fastapi import FastAPI
from app.routers import patient_router

app = FastAPI(title="Patient API")

# include patient router
app.include_router(patient_router.router)
