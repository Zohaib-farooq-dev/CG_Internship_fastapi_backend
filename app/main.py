from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.core.database import Base, engine
from app.routers.patient_router import router as patient_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    print('new tables created')
    Base.metadata.create_all(bind=engine)
    yield  

app = FastAPI(lifespan=lifespan)
app.include_router(patient_router)
