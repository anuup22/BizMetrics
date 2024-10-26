from sqlalchemy.orm import Session
from . import models, schemas
from .auth import get_password_hash

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = models.User(username=user.username, email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

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