from .celery import celery_app
from .database import SessionLocal
from . import models

@celery_app.task
def process_turnover_file(file_path: str):
    db = SessionLocal()
    # Process file and save to database
    db.close()