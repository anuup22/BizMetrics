from sqlalchemy.orm import Session
from . import models, schemas

def get_turnover(db: Session, turnover_id: int):
    return db.query(models.Turnover).filter(models.Turnover.id == turnover_id).first()

def get_turnovers(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Turnover).offset(skip).limit(limit).all()

def create_turnover(db: Session, turnover: schemas.TurnoverCreate):
    db_turnover = models.Turnover(**turnover.dict())
    db.add(db_turnover)
    db.commit()
    db.refresh(db_turnover)
    return db_turnover