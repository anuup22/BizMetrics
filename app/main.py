from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from . import models, schemas, crud
from .database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.post("/turnovers/", response_model=schemas.Turnover)
def create_turnover(turnover: schemas.TurnoverCreate, db: Session = Depends(get_db)):
    return crud.create_turnover(db=db, turnover=turnover)

@app.get("/turnovers/", response_model=list[schemas.Turnover])
def read_turnovers(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    turnovers = crud.get_turnovers(db, skip=skip, limit=limit)
    return turnovers

@app.get("/turnovers/{turnover_id}", response_model=schemas.Turnover)
def read_turnover(turnover_id: int, db: Session = Depends(get_db)):
    db_turnover = crud.get_turnover(db, turnover_id=turnover_id)
    if db_turnover is None:
        raise HTTPException(status_code=404, detail="Turnover not found")
    return db_turnover