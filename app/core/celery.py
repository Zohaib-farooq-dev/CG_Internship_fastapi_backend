from dotenv import load_dotenv
from celery import Celery
import os

load_dotenv()
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

celery_app = Celery(
    "backend_worker",
    broker=REDIS_URL,
    #backend=REDIS_URL,   # optional result backend
)
celery_app.autodiscover_tasks(["app.services.celery_task"])
